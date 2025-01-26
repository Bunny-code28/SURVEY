import sqlite3
from tabulate import tabulate  # You might need to install this: pip install tabulate

def view_formatted_tables():
    conn = sqlite3.connect('survey_database.db')
    cursor = conn.cursor()

    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        print(f"\n{'='*50}")
        print(f"{table_name.upper()} TABLE")
        print(f"{'='*50}")
        
        # Get column names
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]
        
        # Get all rows
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        # Print formatted table
        print(tabulate(rows, headers=column_names, tablefmt='grid'))
        print(f"\nTotal rows: {len(rows)}")

    conn.close()

if __name__ == "__main__":
    view_formatted_tables()