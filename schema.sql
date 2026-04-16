DROP DATABASE IF EXISTS fantasy_league_manager;
CREATE DATABASE fantasy_league_manager;
USE fantasy_league_manager;

CREATE TABLE League (
    league_id INT AUTO_INCREMENT PRIMARY KEY,
    league_name VARCHAR(100) NOT NULL,
    season_year INT NOT NULL,
    UNIQUE (league_name, season_year)
);

CREATE TABLE Owner (
    owner_id INT AUTO_INCREMENT PRIMARY KEY,
    owner_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE Team (
    team_id INT AUTO_INCREMENT PRIMARY KEY,
    league_id INT NOT NULL,
    owner_id INT NOT NULL,
    team_name VARCHAR(100) NOT NULL,
    wins INT DEFAULT 0,
    losses INT DEFAULT 0,
    total_points DECIMAL(8,2) DEFAULT 0,
    FOREIGN KEY (league_id) REFERENCES League(league_id),
    FOREIGN KEY (owner_id) REFERENCES Owner(owner_id)
);

CREATE TABLE Player (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    player_name VARCHAR(100) NOT NULL,
    nfl_team VARCHAR(10),
    position VARCHAR(10) NOT NULL
);

CREATE TABLE Roster (
    roster_id INT AUTO_INCREMENT PRIMARY KEY,
    team_id INT NOT NULL,
    player_id INT NOT NULL,
    roster_status VARCHAR(20) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NULL,
    FOREIGN KEY (team_id) REFERENCES Team(team_id),
    FOREIGN KEY (player_id) REFERENCES Player(player_id)
);

CREATE TABLE Matchup (
    matchup_id INT AUTO_INCREMENT PRIMARY KEY,
    league_id INT NOT NULL,
    week_number INT NOT NULL,
    team1_id INT NOT NULL,
    team2_id INT NOT NULL,
    team1_score DECIMAL(8,2) DEFAULT 0,
    team2_score DECIMAL(8,2) DEFAULT 0,
    winner_team_id INT NULL,
    FOREIGN KEY (league_id) REFERENCES League(league_id),
    FOREIGN KEY (team1_id) REFERENCES Team(team_id),
    FOREIGN KEY (team2_id) REFERENCES Team(team_id),
    FOREIGN KEY (winner_team_id) REFERENCES Team(team_id)
);

CREATE TABLE Score (
    score_id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT NOT NULL,
    week_number INT NOT NULL,
    fantasy_points DECIMAL(8,2) NOT NULL,
    FOREIGN KEY (player_id) REFERENCES Player(player_id),
    UNIQUE (player_id, week_number)
);