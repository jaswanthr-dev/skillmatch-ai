"""
test_connection.py
Run it with: python test_connection.py
"""

from db import get_connection

try:
    connection = get_connection()
    print("Connected to MySQL successfully!")

    cursor = connection.cursor()
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()

    print("Tables in database:")
    for table in tables:
        print(" -", table[0])

    cursor.close()
    connection.close()
    print("Connection closed cleanly.")

except Exception as error:
    print("Failed to connect to MySQL.")
    print("Error details:", error)