import sqlite3

def connect_db():
    conn = sqlite3.connect("nhansu.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nhansu (
        cccd TEXT PRIMARY KEY,
        ten TEXT,
        ngaysinh TEXT,
        gioitinh TEXT,
        diachi TEXT
    )
    """)

    conn.commit()
    return conn, cursor