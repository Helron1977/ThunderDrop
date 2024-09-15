import sqlite3


class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('bot_data.db')
        self.c = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            language TEXT
        )
        ''')
        self.c.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            user_id INTEGER PRIMARY KEY,
            points INTEGER,
            infantry INTEGER,
            archer INTEGER,
            cavalry INTEGER,
            wounded_infantry INTEGER,
            wounded_archer INTEGER,
            wounded_cavalry INTEGER
        )
        ''')
        self.conn.commit()

    def save_player(self, player):
        self.c.execute('''
            INSERT OR REPLACE INTO scores (user_id, points, infantry, archer, cavalry, wounded_infantry, wounded_archer, wounded_cavalry)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (player.user_id, player.points, player.infantry, player.archer, player.cavalry, player.wounded_infantry, player.wounded_archer, player.wounded_cavalry))
        self.conn.commit()

    def load_player(self, user_id):
        from player import Player # Import the Player class here to avoid circular import
        self.c.execute('SELECT * FROM scores WHERE user_id = ?', (user_id,))
        result = self.c.fetchone()
        if result:
            # Create a Player object with the loaded data set to default values if no data is found
            return Player(
                user_id=result[0],
                points=result[1] if result[1] is not None else 0,
                infantry=result[2] if result[2] is not None else 0,
                archer=result[3] if result[3] is not None else 0,
                cavalry=result[4] if result[4] is not None else 0,
                wounded_infantry=result[5] if result[5] is not None else 0,
                wounded_archer=result[6] if result[6] is not None else 0,
                wounded_cavalry=result[7] if result[7] is not None else 0
            )
        else:
            return Player(user_id)
    
    def get_all_players(self):
        from player import Player
        self.c.execute('SELECT * FROM scores')
        results = self.c.fetchall()
        players = []
        for result in results:
            player = Player(
                user_id=result[0],
                points=result[1] if result[1] is not None else 0,
                infantry=result[2] if result[2] is not None else 0,
                archer=result[3] if result[3] is not None else 0,
                cavalry=result[4] if result[4] is not None else 0,
                wounded_infantry=result[5] if result[5] is not None else 0,
                wounded_archer=result[6] if result[6] is not None else 0,
                wounded_cavalry=result[7] if result[7] is not None else 0
            )
            players.append(player)
        return players

    def set_user_language(self, user_id, language):
        try:
            self.c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            result = self.c.fetchone()
            if result:
                self.c.execute('UPDATE users SET language = ? WHERE user_id = ?', (language, user_id))
            else:
                self.c.execute('INSERT INTO users (user_id, language) VALUES (?, ?)', (user_id, language))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def __del__(self):
        try:
            self.conn.close()
        except AttributeError:
            pass