from backend.models.db_connect import get_connection

def init_db():
    """Initialize the database with a users table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            gender TEXT,
            favcol TEXT
        )
    """)
    conn.commit()

    cursor.execute("""
            INSERT INTO users (name, email, password, gender, favcol)
            VALUES (?, ?, ?, ?, ?)
        """, ("YH", "yh@email.com", "pw", "f", "yellow"))
    conn.commit()

    cursor.execute("""
            INSERT INTO users (name, email, password, gender, favcol)
            VALUES (?, ?, ?, ?, ?)
        """, ("LG", "lg@email.com", "pw", "m", "yellow"))
    conn.commit()

    cursor.execute("""
            INSERT INTO users (name, email, password, gender, favcol)
            VALUES (?, ?, ?, ?, ?)
        """, ("SG", "sg@email.com", "pw", "m", "yellow"))
    conn.commit()

    conn.close()

init_db()