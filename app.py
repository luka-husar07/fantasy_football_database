from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "fantasy_league_manager")
    )

@app.route("/")
def home():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM League")
    leagues = cursor.fetchall()

    cursor.execute("""
        SELECT t.team_id, t.team_name, o.owner_name, t.wins, t.losses, t.total_points
        FROM Team t
        JOIN Owner o ON t.owner_id = o.owner_id
        ORDER BY t.wins DESC, t.total_points DESC
    """)
    leaderboard = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template("home.html", leagues=leagues, leaderboard=leaderboard)

@app.route("/teams", methods=["GET", "POST"])
def teams():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        league_id = request.form["league_id"]
        owner_id = request.form["owner_id"]
        team_name = request.form["team_name"]

        cursor.execute("""
            INSERT INTO Team (league_id, owner_id, team_name, wins, losses, total_points)
            VALUES (%s, %s, %s, 0, 0, 0)
        """, (league_id, owner_id, team_name))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for("teams"))

    cursor.execute("""
        SELECT t.team_id, t.team_name, o.owner_name, t.wins, t.losses, t.total_points
        FROM Team t
        JOIN Owner o ON t.owner_id = o.owner_id
        ORDER BY t.team_id
    """)
    teams = cursor.fetchall()

    cursor.execute("SELECT * FROM Owner")
    owners = cursor.fetchall()

    cursor.execute("SELECT * FROM League")
    leagues = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template("teams.html", teams=teams, owners=owners, leagues=leagues)

@app.route("/add_owner", methods=["POST"])
def add_owner():
    owner_name = request.form["owner_name"]
    email = request.form["email"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Owner (owner_name, email)
        VALUES (%s, %s)
    """, (owner_name, email))
    conn.commit()

    cursor.close()
    conn.close()
    return redirect(url_for("teams"))

@app.route("/delete_team", methods=["POST"])
def delete_team():
    team_id = request.form["team_id"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Team WHERE team_id = %s", (team_id,))
    conn.commit()

    cursor.close()
    conn.close()
    return redirect(url_for("teams"))

@app.route("/team/<int:team_id>/roster")
def roster(team_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Team WHERE team_id = %s", (team_id,))
    team = cursor.fetchone()

    cursor.execute("""
        SELECT r.roster_id, p.player_name, p.nfl_team, p.position, r.roster_status, r.start_date, r.end_date
        FROM Roster r
        JOIN Player p ON r.player_id = p.player_id
        WHERE r.team_id = %s AND r.end_date IS NULL
        ORDER BY p.position, p.player_name
    """, (team_id,))
    players = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template("roster.html", team=team, players=players)

@app.route("/free_agents")
def free_agents():
    position = request.args.get("position", "")
    selected_team_id = request.args.get("team_id", "")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if position:
        cursor.execute("""
            SELECT p.*
            FROM Player p
            WHERE p.position = %s
                AND p.player_id NOT IN (
                    SELECT player_id FROM Roster WHERE end_date IS NULL
                )
            ORDER BY p.player_name
        """, (position,))
    else:
        cursor.execute("""
            SELECT p.*
            FROM Player p
            WHERE p.player_id NOT IN (
                SELECT player_id FROM Roster WHERE end_date IS NULL
            )
            ORDER BY p.position, p.player_name
        """)

    agents = cursor.fetchall()

    cursor.execute("SELECT team_id, team_name FROM Team")
    teams = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("free_agents.html", free_agents=agents, 
                           selected_position=position, teams=teams, 
                           selected_team_id=selected_team_id)

@app.route("/update_roster_status", methods=["POST"])
def update_roster_status():
    roster_id = request.form["roster_id"]
    new_status = request.form["roster_status"]
    team_id = request.form["team_id"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE Roster
        SET roster_status = %s
        WHERE roster_id = %s
    """, (new_status, roster_id))
    conn.commit()

    cursor.close()
    conn.close()
    return redirect(url_for("roster", team_id=team_id))

@app.route("/drop_player", methods=["POST"])
def drop_player():
    roster_id = request.form["roster_id"]
    team_id = request.form["team_id"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE Roster
        SET end_date = CURDATE()
        WHERE roster_id = %s
    """, (roster_id,))
    conn.commit()

    cursor.close()
    conn.close()
    return redirect(url_for("roster", team_id=team_id))

@app.route("/sign_player", methods=["POST"])
def sign_player():
    player_id = request.form["player_id"]
    team_id = request.form["team_id"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Roster (team_id, player_id, roster_status, start_date)
        VALUES (%s, %s, 'Active', CURDATE())
    """, (team_id, player_id))
    conn.commit()

    cursor.close()
    conn.close()
    return redirect(url_for("free_agents"))

@app.route("/recommend/<int:team_id>")
def recommend(team_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Team WHERE team_id = %s", (team_id,))
    team = cursor.fetchone()

    # Find weakest position on roster
    cursor.execute("""
        SELECT p.position, AVG(s.fantasy_points) AS avg_points
        FROM Roster r
        JOIN Player p ON r.player_id = p.player_id
        JOIN Score s ON p.player_id = s.player_id
        WHERE r.team_id = %s
          AND r.end_date IS NULL
        GROUP BY p.position
        ORDER BY avg_points ASC
        LIMIT 1
    """, (team_id,))
    weakest = cursor.fetchone()

    recommendation = None

    if weakest:
        cursor.execute("""
            SELECT p.player_id, p.player_name, p.nfl_team, p.position,
                   AVG(s.fantasy_points) AS avg_points
            FROM Player p
            LEFT JOIN Score s ON p.player_id = s.player_id
            WHERE p.position = %s
              AND p.player_id NOT IN (
                  SELECT player_id
                  FROM Roster
                  WHERE end_date IS NULL
              )
            GROUP BY p.player_id, p.player_name, p.nfl_team, p.position
            ORDER BY avg_points DESC
            LIMIT 1
        """, (weakest["position"],))
        recommendation = cursor.fetchone()

    cursor.close()
    conn.close()
    return render_template(
        "recommendations.html",
        team=team,
        weakest=weakest,
        recommendation=recommendation
    )

if __name__ == "__main__":
    app.run(debug=True)