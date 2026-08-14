"""
=========================================================
Database Manager
AI-Powered Job Posting Analyzer
=========================================================
"""

import sqlite3
from pathlib import Path

# --------------------------------------------------------
# Paths
# --------------------------------------------------------

DATABASE_FOLDER = Path(__file__).parent

DATABASE_FILE = DATABASE_FOLDER / "app.db"

SCHEMA_FILE = DATABASE_FOLDER / "schema.sql"


# --------------------------------------------------------
# Database Manager
# --------------------------------------------------------

class DatabaseManager:

    def __init__(self):

        self.connection = sqlite3.connect(
            DATABASE_FILE,
            check_same_thread=False
        )

        self.connection.row_factory = sqlite3.Row

        self.create_tables()

    # ----------------------------------------------------
    # Create Tables
    # ----------------------------------------------------

    def create_tables(self):

        with open(
            SCHEMA_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            schema = file.read()

        self.connection.executescript(schema)

        self.connection.commit()

    # ----------------------------------------------------
    # Execute Query
    # ----------------------------------------------------

    def execute(
        self,
        query,
        values=()
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            query,
            values
        )

        self.connection.commit()

        return cursor

    # ----------------------------------------------------
    # Fetch All
    # ----------------------------------------------------

    def fetchall(
    self,
    query,
    values=()
):
        cursor = self.connection.cursor()

        cursor.execute(
            query,
            values
        )

        return cursor.fetchall()

    # ----------------------------------------------------
    # Close Connection
    # ----------------------------------------------------

    def close(self):

        self.connection.close()