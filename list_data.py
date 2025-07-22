import sqlite3
import os

def list_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "voice_dataset.db")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT id, question, answer, answer_audio_path FROM qa_pairs")
    rows = cursor.fetchall()

    if not rows:
        print("❌ No data found.")
        conn.close()
        return

    while True:
        print("\n📋 Stored Q&A Pairs:\n" + "-"*60)
        for i, row in enumerate(rows, start=1):
            print(f"🔢 Sr#: {i}")
            print(f"❓ Question: {row[1]}")
            print(f"💬 Answer: {row[2]}")
            print("-" * 60)

        delete_choice = input("\n🗑️ Do you want to delete any entry? (y/n): ").strip().lower()
        if delete_choice != 'y':
            break

        try:
            sr_number = int(input("Enter the Sr# of the entry to delete: ").strip())
            if 1 <= sr_number <= len(rows):
                entry = rows[sr_number - 1]
                delete_id = entry[0]
                audio_path = entry[3]

                # Delete audio file if it exists
                if audio_path:
                    abs_audio_path = os.path.abspath(audio_path)
                    if os.path.exists(abs_audio_path):
                        os.remove(abs_audio_path)
                        print(f"🗑️ Deleted audio file: {abs_audio_path}")
                    else:
                        print(f"⚠️ Audio file not found: {abs_audio_path}")

                # Delete from database
                cursor.execute("DELETE FROM qa_pairs WHERE id=?", (delete_id,))
                conn.commit()
                print("✅ Entry deleted successfully!")

                # Refresh rows after deletion
                cursor.execute("SELECT id, question, answer, answer_audio_path FROM qa_pairs")
                rows = cursor.fetchall()

                if not rows:
                    print("✅ All entries deleted.")
                    break
            else:
                print("❌ Invalid Sr#.")
        except ValueError:
            print("❌ Please enter a valid number.")

    conn.close()

if __name__ == "__main__":
    list_data()
