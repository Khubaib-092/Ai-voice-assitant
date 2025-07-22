
def classify_intent(user_query: str) -> str:
    """
    Simple rule-based intent classification.
    You can later upgrade to ML-based classifier.
    """
    query = user_query.lower()

    if any(word in query for word in ["hello", "hi", "salam", "assalamualaikum"]):
        return "greeting"
    if any(word in query for word in ["policy", "rule", "document", "profile", "company", "information"]):
        return "document_query"
    if any(word in query for word in ["thanks", "shukriya", "thank you"]):
        return "thanks"
    # Default fallback
    return "general"
