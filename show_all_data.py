import sqlite3

conn = sqlite3.connect("voice_data.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM voice_data")
rows = cursor.fetchall()

if rows:
    for row in rows:
        print(f"🟢 ID: {row[0]}")
        print(f"🧠 Question: {row[1]}")
        print(f"💬 Answer: {row[2]}")
        print("-" * 40)
else:
    print("❌ No rows found.")

conn.close()
