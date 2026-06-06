import sqlite3
from datetime import datetime


class Database:

    def __init__(self):

        self.conn = sqlite3.connect(
            "database/vision.db"
        )

        self.create_table()

    def create_table(self):

        cursor = self.conn.cursor()

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS inspection_history(
            id INTEGER PRIMARY KEY,
            datetime TEXT,
            recipe TEXT,
            result TEXT,
            reason TEXT,
            score REAL,
            image_path TEXT
        )

        """)

        self.conn.commit()

    def add_result(
        self,
        recipe,
        result,
        ng_reason,
        score,
        image_path
    ):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT INTO inspection_history
            (
                datetime,
                recipe,
                result,
                reason,
                score,
                image_path
            )
            VALUES
            (
                ?,
                ?,
                ?,
                ?,
                ?,
                ?
            )
            """,
            (
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                recipe,
                result,
                ng_reason,
                score,
                image_path
            )
        )

        self.conn.commit()
    
    def get_all(self):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM inspection_history
            ORDER BY id DESC
            """
        )

        return cursor.fetchall()

    def search_result(
        self,
        result
    ):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM inspection_history
            WHERE result = ?
            ORDER BY id DESC
            """,
            (
                result,
            )
        )

        return cursor.fetchall()
    
    def search_recipe(
        self,
        recipe
    ):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM inspection_history
            WHERE recipe = ?
            ORDER BY id DESC
            """,
            (
                recipe,
            )
        )

        return cursor.fetchall()
    
    def get_last_results(
        self,
        limit=50
    ):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT result
            FROM inspection_history
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )
        return cursor.fetchall()