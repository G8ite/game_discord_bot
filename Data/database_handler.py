import os
import sqlite3

class DatabaseHandler():
    def __init__(self, database_name:str):
        self.con = sqlite3.connect(f"{database_name}")
        self.con.row_factory = sqlite3.Row

    def add_user(self, user_name: str):
        cursor = self.con.cursor()
        query = "INSERT INTO user (name) VALUES (?); "
        try:
            cursor.execute(query, (user_name,))
        except:
            return 0
        cursor.close()
        self.con.commit()