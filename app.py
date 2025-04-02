from flask import Flask, jsonify, request
import requests
import time
from collections import deque

app = Flask(__name__)

WINDOW_SIZE = 10
number_window = deque(maxlen=WINDOW_SIZE)

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzQzNTk5OTUzLCJpYXQiOjE3NDM1OTk2NTMsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6IjMyNTkwNGY2LTk2NTctNDM2My04NmM2LWZjMjMwZDFhZDg2OCIsInN1YiI6IjIyMjkwNzVAa2lpdC5hYy5pbiJ9LCJlbWFpbCI6IjIyMjkwNzVAa2lpdC5hYy5pbiIsIm5hbWUiOiJzcmluamF5ZWUgcGF1bCIsInJvbGxObyI6IjIyMjkwNzUiLCJhY2Nlc3NDb2RlIjoibndwd3JaIiwiY2xpZW50SUQiOiIzMjU5MDRmNi05NjU3LTQzNjMtODZjNi1mYzIzMGQxYWQ4NjgiLCJjbGllbnRTZWNyZXQiOiJHRmZBd0hOVXVBbkdiUWRCIn0.cquRhhKnUso1m5s7PBZA-9vpqbIlXV8yxbIizdla8HY"

API_URLS = {
    "p": "http://20.244.56.144/evaluation-service/primes",
    "f": "http://20.244.56.144/evaluation-service/fibo",
    "e": "http://20.244.56.144/evaluation-service/even",
    "r": "http://20.244.56.144/evaluation-service/rand",
}

def fetch_numbers(number_type):
    """
    Fetch numbers from the test server, ensuring:
    - Authorization token is included.
    - Response time is less than 500ms.
    - Only valid responses are returned.
    """
    url = API_URLS.get(number_type)
    if not url:
        return None 

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    try:
        start_time = time.time()
        response = requests.get(url, headers=headers, timeout=0.5)
        end_time = time.time()

        # Debugging logs
        print(f"Fetching from: {url}")
        print(f"Status Code: {response.status_code}")
        print(f"Time Taken: {end_time - start_time}")
        print(f"Response: {response.text}")

        if response.status_code == 200 and (end_time - start_time) <= 0.5:
            return response.json().get("numbers", [])

        print("Ignoring slow response or bad status code.")
        return None 
    except requests.exceptions.RequestException as e:
        print(f"Error fetching numbers: {e}")
        return None 

@app.route("/numbers/<number_id>", methods=["GET"])
def get_numbers(number_id):
    """
    Handles requests to fetch numbers, maintain a sliding window,
    and return the average.
    """
    if number_id not in API_URLS:
        return jsonify({"error": "Invalid number ID"}), 400

    prev_state = list(number_window)

    fetched_numbers = fetch_numbers(number_id)
    if fetched_numbers is None:
        return jsonify({"error": "Failed to fetch numbers"}), 500

    for num in fetched_numbers:
        if num not in number_window:
            number_window.append(num)

    curr_state = list(number_window)

    avg = round(sum(curr_state) / len(curr_state), 2) if curr_state else 0

    response = {
        "windowPrevState": prev_state,
        "windowCurrState": curr_state,
        "numbers": fetched_numbers,
        "avg": avg
    }

    return jsonify(response), 200

if __name__ == "__main__":
    app.run(host="localhost", port=9876, debug=True)
