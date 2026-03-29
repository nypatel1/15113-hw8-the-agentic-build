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
        result = self.cursor.fetchone()[0]
        return result if result is not None else 0

    def get_best_score(self, username):
        self.cursor.execute('''
            SELECT MAX(score) FROM scores WHERE username = ?
        ''', (username,))
        result = self.cursor.fetchone()[0]
        return result if result is not None else 0

    def get_recent_scores(self, username, limit=10):
        """Get the last N scores for a user."""
        self.cursor.execute('''
            SELECT score FROM scores WHERE username = ?
            ORDER BY timestamp DESC LIMIT ?
        ''', (username, limit))
        return [row[0] for row in self.cursor.fetchall()]

    def render_chart(self, username):
        """Render ASCII bar chart of last 10 quiz scores for the user."""
        scores = self.get_recent_scores(username, 10)
        
        if not scores:
            print("No quiz scores yet.")
            return
        
        scores.reverse()  # Show chronologically
        print("\n=== Your Last 10 Quiz Scores ===")
        
        for i, score in enumerate(scores, 1):
            bar_length = int(score / 10 * 30)  # Scale to max 30 chars
            bar = "█" * bar_length
            print(f"Quiz {i:2d}: {bar} {score:.1f}")
        
        print(f"\nAverage: {self.compute_average_score(username):.1f}")
        print(f"Best: {self.get_best_score(username):.1f}")

    def close(self):
        self.connection.close()