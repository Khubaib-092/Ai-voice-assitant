import sqlite3

def search_data():
    conn = sqlite3.connect("voice_dataset.db")
    cursor = conn.cursor()

    keyword = input("🔎 Enter a keyword to search: ").strip()

    query = """
    SELECT id, question, answer FROM qa_pairs
    WHERE question LIKE ? OR answer LIKE ?
    """
    wildcard_keyword = f"%{keyword}%"
    cursor.execute(query, (wildcard_keyword, wildcard_keyword))

    results = cursor.fetchall()

    if results:
        print("\n📋 Matching Results:\n" + "-"*40)
        for row in results:
            print(f"🆔 ID: {row[0]}")
            print(f"❓ Question: {row[1]}")
            print(f"💬 Answer: {row[2]}")
            print("-" * 40)
    else:
        print("❌ No results found for your keyword.")

    conn.close()

if __name__ == "__main__":
    search_data()
