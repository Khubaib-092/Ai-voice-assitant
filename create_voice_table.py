import sqlite3

conn = sqlite3.connect("voice_data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS voice_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("✅ voice_data table created successfully!")
