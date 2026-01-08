import sqlite3
import bcrypt
import json

from .profile_manager import ProfileManager


class AccountManager:
    def __init__(self):
        self.con: sqlite3.Connection | None = None
        self.cur: sqlite3.Cursor | None = None

        self.current_account: int | None = None

        self.profile_manager = ProfileManager()
        self.profile_manager.file_path = 'database/data.json'

        self.connect_to_db()

    def connect_to_db(self):
        self.con = sqlite3.connect('database/parafect_db.db')
        self.cur = self.con.cursor()

    def close_db(self):
        self.con.close()

    def add_account(self, login, password):
        coded_password = self.code_password(password)
        self.cur.execute("""INSERT INTO Users(login, password) VALUES (?, ?)""", (login, coded_password))
        self.con.commit()

        user_id = self.cur.lastrowid
        self.profile_manager.create_profile(user_id)

        return user_id

    def get_account(self, login, password):
        self.cur.execute(f"""
        SELECT
            id,
            login,
            password
        FROM Users
            WHERE login = '{login}'
    """)
        res = self.cur.fetchone()

        if not res:
            return False

        user_id, db_login, db_password = res

        if self.check_password(password, db_password):
            self.current_account = user_id

            profile = self.profile_manager.load_profile(user_id)
            return {'suc': True, 'user_id': user_id, 'profile': profile}
        else:
            return False

    def get_data(self):
        if not self.current_account:
            return None

        profile = self.profile_manager.load_profile(self.current_account)

        self.cur.execute("""
                SELECT login 
                FROM Users 
                WHERE id = ?
            """, (self.current_account,))

        result = self.cur.fetchone()

        if result and profile:
            return {
                "id": self.current_account,
                "login": result[0],
                "profile": profile
            }
        return None

    def update_profile(self, profile_data):
        if not self.current_account:
            return False

        return self.profile_manager.save_profile(self.current_account, profile_data)

    def get_logins(self):
        return [a for b in self.cur.execute("""SELECT login FROM Users""") for a in b]

    @staticmethod
    def code_password(password: str) -> str:
        bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        coded_password = bcrypt.hashpw(bytes, salt)
        return coded_password.decode()

    @staticmethod
    def check_password(password: str, coded_password: str) -> bool:
        try:
            bytes = password.encode('utf-8')
            coded_bytes = coded_password.encode('utf-8')

            return bcrypt.checkpw(bytes, coded_bytes)
        except:
            return False
