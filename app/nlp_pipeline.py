from app.document_search import search_documents

def process_user_query(user_text: str) -> str:
    results = search_documents(user_text, top_k=1)
    if results:
        return results[0]
    else:
        return "معذرت! میں اس سوال کا جواب فی الحال نہیں دے سکتا۔"
