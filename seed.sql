USE fantasy_league_manager;

INSERT INTO League (league_name, season_year)
VALUES ('FSU Fantasy League', 2025);

INSERT INTO Owner (owner_name, email) VALUES
('Luka Husar', 'luka@example.com'),
('Alex Carter', 'alex@example.com'),
('Jamie Brooks', 'jamie@example.com'),
('Taylor Reed', 'taylor@example.com');

INSERT INTO Team (league_id, owner_id, team_name, wins, losses, total_points) VALUES
(1, 1, 'Tallahassee Touchdowns', 2, 1, 312.50),
(1, 2, 'Capital City Crushers', 1, 2, 287.90),
(1, 3, 'Seminole Stars', 3, 0, 341.20),
(1, 4, 'Fourth and Goal', 0, 3, 250.60);

INSERT INTO Player (player_name, nfl_team, position) VALUES
('Josh Allen', 'BUF', 'QB'),
('Jalen Hurts', 'PHI', 'QB'),
('Christian McCaffrey', 'SF', 'RB'),
('Bijan Robinson', 'ATL', 'RB'),
('Justin Jefferson', 'MIN', 'WR'),
('CeeDee Lamb', 'DAL', 'WR'),
('Travis Kelce', 'KC', 'TE'),
('Sam LaPorta', 'DET', 'TE'),
('Joe Burrow', 'CIN', 'QB'),
('Breece Hall', 'NYJ', 'RB'),
('Amon-Ra St. Brown', 'DET', 'WR'),
('Mark Andrews', 'BAL', 'TE'),
('Dak Prescott', 'DAL', 'QB'),
('DeVonta Smith', 'PHI', 'WR'),
('Rachaad White', 'TB', 'RB'),
('Evan Engram', 'JAX', 'TE');

INSERT INTO Roster (team_id, player_id, roster_status, start_date, end_date) VALUES
(1, 1, 'Starter', '2025-09-01', NULL),
(1, 3, 'Starter', '2025-09-01', NULL),
(1, 5, 'Starter', '2025-09-01', NULL),
(1, 7, 'Starter', '2025-09-01', NULL),

(2, 2, 'Starter', '2025-09-01', NULL),
(2, 4, 'Starter', '2025-09-01', NULL),
(2, 6, 'Starter', '2025-09-01', NULL),
(2, 8, 'Starter', '2025-09-01', NULL),

(3, 9, 'Starter', '2025-09-01', NULL),
(3, 10, 'Starter', '2025-09-01', NULL),
(3, 11, 'Starter', '2025-09-01', NULL),
(3, 12, 'Starter', '2025-09-01', NULL);

-- Team 4 intentionally weaker / incomplete for demo purposes

INSERT INTO Score (player_id, week_number, fantasy_points) VALUES
(1, 1, 24.5), (1, 2, 22.0), (1, 3, 26.4),
(2, 1, 21.3), (2, 2, 19.8), (2, 3, 24.1),
(3, 1, 18.0), (3, 2, 16.7), (3, 3, 20.4),
(4, 1, 14.2), (4, 2, 12.1), (4, 3, 17.0),
(5, 1, 19.5), (5, 2, 21.1), (5, 3, 20.0),
(6, 1, 17.8), (6, 2, 18.2), (6, 3, 15.9),
(7, 1, 11.0), (7, 2, 9.8),  (7, 3, 10.4),
(8, 1, 13.2), (8, 2, 14.5), (8, 3, 12.9),
(9, 1, 18.3), (9, 2, 22.4), (9, 3, 19.6),
(10, 1, 15.7), (10, 2, 13.9), (10, 3, 16.8),
(11, 1, 20.1), (11, 2, 18.7), (11, 3, 21.6),
(12, 1, 8.4), (12, 2, 7.9), (12, 3, 9.1),
(13, 1, 23.0), (13, 2, 25.2), (13, 3, 21.7),
(14, 1, 14.0), (14, 2, 16.1), (14, 3, 13.7),
(15, 1, 10.5), (15, 2, 12.2), (15, 3, 11.9),
(16, 1, 9.6), (16, 2, 11.3), (16, 3, 10.8);

INSERT INTO Matchup (league_id, week_number, team1_id, team2_id, team1_score, team2_score, winner_team_id) VALUES
(1, 1, 1, 2, 104.3, 97.1, 1),
(1, 1, 3, 4, 112.6, 80.2, 3),
(1, 2, 1, 3, 99.8, 110.3, 3),
(1, 2, 2, 4, 95.4, 82.5, 2),
(1, 3, 1, 4, 108.4, 87.9, 1),
(1, 3, 2, 3, 95.4, 118.3, 3);