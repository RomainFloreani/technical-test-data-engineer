import sqlite3
from tabulate import tabulate  # optional for pretty print

DB_PATH = "music_data.db"
TABLES = ["tracks", "users", "listen_history"]

def show_table_data(conn, table):
    print(f"\n🔎 Table: {table}")
    try:
        cursor = conn.execute(f"SELECT * FROM {table} LIMIT 5")
        rows = cursor.fetchall()
        headers = [description[0] for description in cursor.description]
        if rows:
            print(tabulate(rows, headers=headers, tablefmt="pretty"))
        else:
            print("⚠️ No rows found.")
    except Exception as e:
        print(f"❌ Error reading table {table}: {e}")

def debug_all_tables():
    conn = sqlite3.connect(DB_PATH)
    for table in TABLES:
        show_table_data(conn, table)
    conn.close()

if __name__ == "__main__":
    debug_all_tables()