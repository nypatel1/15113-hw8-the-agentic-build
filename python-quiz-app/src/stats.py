import sqlite3

class Stats:
    def __init__(self, db_path='data/scores.db'):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                score INTEGER NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.connection.commit()

    def add_score(self, username, score):
        self.cursor.execute('''
            INSERT INTO scores (username, score) VALUES (?, ?)
        ''', (username, score))
        self.connection.commit()

    def get_scores(self, username):
        self.cursor.execute('''
            SELECT score, timestamp FROM scores WHERE username = ?
        ''', (username,))
        return self.cursor.fetchall()

    def compute_average_score(self, username):
        self.cursor.execute('''
            SELECT AVG(score) FROM scores WHERE username = ?
        ''', (username,))
        return self.cursor.fetchone()[0]

    def close(self):
        self.connection.close()