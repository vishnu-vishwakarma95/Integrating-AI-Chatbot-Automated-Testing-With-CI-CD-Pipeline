import requests
import json
import os

API_URL = "https://api.openai.com/v1/engines/gpt-3.5-turbo/completions"  # Updated API URL
API_KEY = os.getenv("PUT YOUR KEY HERE")

def ask_chatbot(question):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": question,
        "max_tokens": 50
    }
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    return None

def load_expected_responses(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

def test_chatbot_responses():
    expected_responses = load_expected_responses('/home/nashtech/chatbot-testing/data/expected_responses.json')
    with open('/home/nashtech/chatbot-testing/test_results.txt', 'w') as f:
        f.write("Question | Expected Response | Actual Response | Result\n")
        for question, expected_answer in expected_responses.items():
            response = ask_chatbot(question)
            actual_answer = response.get('choices')[0].get('text').strip()
            result = "Passed" if actual_answer == expected_answer else "Failed"
            f.write(f"{question} | {expected_answer} | {actual_answer} | {result}\n")

if __name__ == "__main__":
    test_chatbot_responses()
