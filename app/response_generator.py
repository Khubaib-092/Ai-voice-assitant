
def generate_response(intent, doc_result=None, llm_result=None):
    if intent == "greeting":
        return "Walikum Salam! How can I assist you today?"

    if intent == "thanks":
        return "You're most welcome! Always here to help."

    if doc_result:
        return f"According to our documents: {doc_result}"

    if llm_result:
        return llm_result

    return "I'm sorry, I don't have information on that right now."
