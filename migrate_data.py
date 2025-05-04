import pandas as pd
import sqlite3

def init_database():
    """Initialize SQLite database and create necessary tables"""
    with sqlite3.connect('chi_database.db') as conn:
            cursor = conn.cursor()
            # Create main chi_table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS chi_table (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    mychi INTEGER,
                    gap INTEGER,
                    continuity INTEGER,
                    date TEXT,
                    mode TEXT,
                    reminder INTEGER
                )
            ''')
            conn.commit()



def migrate_csv_to_sqlite():
    # Read existing CSV data
    df = pd.read_csv('chi_data.csv')
    
    # Connect to SQLite database
    with sqlite3.connect('chi_database.db') as conn:
        # Create tables
        df.to_sql('chi_table', conn, if_exists='replace', index=False)

if __name__ == "__main__":
    init_database()
    migrate_csv_to_sqlite()