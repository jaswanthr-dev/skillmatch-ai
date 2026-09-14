"""
db.py

This module handles connecting to our MySQL database.

Why this is a separate file: every other part of the app (saving an
analysis, viewing history, deleting an entry) will need a database
connection. Instead of repeating connection code everywhere, we write
it once here and reuse it.
"""

import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    """
    Opens and returns a new connection to the MySQL database.

    Why DB_PORT has a default of 3306: that's MySQL's standard port,
    used by most local installs. Hosted providers like Aiven often
    use a different, non-standard port, so DB_PORT lets us override
    it via .env without touching this code.
    """
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        ssl_disabled=False,
    )
    return connection