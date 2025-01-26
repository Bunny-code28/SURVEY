import sqlite3

try:
    # Connect to database (creates if not exists)
    conn = sqlite3.connect('survey_database.db')
    cursor = conn.cursor()

    # SQL commands
    sql_commands = """
    -- USERS TABLE
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        user_id VARCHAR(255),
        password VARCHAR(255),
        name VARCHAR(255),
        email VARCHAR(255)
    );

    -- ADMIN TABLE
    CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY,
        username VARCHAR(255),
        password VARCHAR(255),
        email VARCHAR(255),
        role VARCHAR(50)
    );

    -- SURVEYS TABLE
    CREATE TABLE IF NOT EXISTS surveys (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        topic VARCHAR(255),
        answers TEXT,
        timestamp DATETIME,
        email VARCHAR(255)
    );
    """

    # Execute SQL commands for table creation
    cursor.executescript(sql_commands)

    # Insert users data
    users_data = [
        (1, 'chanduvk133@gmail.com', 'pbkdf2:sha256:260000$YIrm9zkZdkBG41tt$381aa80b5ba388d6fb64f8969707f58f43615eff89d01fed19fa5333820dfebf', 'abhishek', 'chanduvk133@gmail.com'),
        (2, 'reni@gmail.com', 'pbkdf2:sha256:260000$Dg9xeDScJWirN0BN$5f8898f418621e253852f7573ca0efb7151204b649c6efa81f2315a4b320f7d9', 'reni', 'reni@gmail.com'),
        # Add all other users here
    ]
    cursor.executemany('INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?, ?)', users_data)

    # Insert admin data
    admin_data = [('admin', 'hashed_password_here', 'admin@example.com', 'superadmin')]
    cursor.executemany('INSERT OR REPLACE INTO admin (username, password, email, role) VALUES (?, ?, ?, ?)', admin_data)

    # Insert surveys data
    surveys_data = [
        (1, 1, 'sports', '{"q1": "rarely", "q2": "football", "q3": "Football", "q4": "No", "q5": "yes"}', '2024-10-17 01:26:11', None),
        (2, 1, 'sports', '{"q1": "daily", "q2": "football", "q3": "Cricket", "q4": "No", "q5": "no"}', '2024-10-17 01:33:09', None),
        # Add all other surveys here
    ]
    cursor.executemany('INSERT OR REPLACE INTO surveys VALUES (?, ?, ?, ?, ?, ?)', surveys_data)

    # Commit changes
    conn.commit()
    print("Database created successfully!")

except sqlite3.Error as e:
    print(f"An error occurred: {e}")

finally:
    # Close connection
    if conn:
        conn.close()
        print("Database connection closed.")