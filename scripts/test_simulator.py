import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.nlp_pipeline import process_user_query

print("=== AI Assistant Simulation ===")
while True:
    user_input = input("\nUser: ")
    if user_input.lower() in ['exit', 'quit', 'bye']:
        print("Goodbye!")
        break
    response = process_user_query(user_input)
    print(f"Assistant: {response}")
