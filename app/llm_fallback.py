import requests

# ✅ Store API key in a variable (this is correct)
OPENROUTER_API_KEY = "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"

def query_openrouter(prompt: str):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",  # ✅ This is the correct way
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    result = response.json()
    return result['choices'][0]['message']['content']
