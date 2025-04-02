from flask import Flask, jsonify, request
import requests
import time
from collections import deque

app = Flask(__name__)

WINDOW_SIZE = 10

number_window = deque(maxlen=WINDOW_SIZE)

API_URLS = {
    "p": "http://20.244.56.144/evaluation-service/primes",
    "f": "http://20.244.56.144/evaluation-service/fibo",
    "e": "http://20.244.56.144/evaluation-service/even",
    "r": "http://20.244.56.144/evaluation-service/rand",
}

def fetch_numbers(number_type):
    """Fetch numbers from the test server, ensuring a response time < 500ms."""
    url = API_URLS.get(number_type)
    if not url:
        return None

    try:
        start_time = time.time()
        response = requests.get(url, timeout=0.5) 
        end_time = time.time()

        if response.status_code == 200 and (end_time - start_time) <= 0.5:
            return response.json().get("numbers", [])
        return None 
    except requests.exceptions.RequestException:
        return None  #b

@app.route("/numbers/<number_id>", methods=["GET"])
def get_numbers(number_id):
    """Handle requests to fetch and store numbers."""
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
