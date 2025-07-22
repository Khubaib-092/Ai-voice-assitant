import sqlite3
import csv
import json

def export_to_csv(data):
    with open("exported_data.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Question", "Answer", "Answer Audio Path"])
        writer.writerows(data)
    print("✅ Data exported to exported_data.csv")

def export_to_json(data):
    data_list = [
        {"id": row[0], "question": row[1], "answer": row[2], "audio_path": row[3]}
        for row in data
    ]
    with open("exported_data.json", "w", encoding="utf-8") as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)
    print("✅ Data exported to exported_data.json")

def export_data():
    conn = sqlite3.connect("voice_dataset.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM qa_pairs")  # ✅ Fixed table name
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("❌ No data found to export.")
        return

    print("📦 Choose export format:")
    print("1. CSV")
    print("2. JSON")
    choice = input("Enter choice (1/2): ").strip()

    if choice == "1":
        export_to_csv(rows)
    elif choice == "2":
        export_to_json(rows)
    else:
        print("❌ Invalid choice.")

if __name__ == "__main__":
    export_data()
