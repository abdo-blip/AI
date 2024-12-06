from flask import Flask, jsonify
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST, start_http_server
import random

app = Flask(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter('flask_app_requests_total', 'Total requests count', ['method', 'endpoint'])
SUCCESS_COUNT = Counter('flask_app_success_total', 'Successful requests count')
ERROR_COUNT = Counter('flask_app_error_total', 'Error requests count')

@app.route('/')
def home():
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    SUCCESS_COUNT.inc()
    return jsonify({"message": "Welcome to the Flask App!"})

@app.route('/data')
def data():
    REQUEST_COUNT.labels(method='GET', endpoint='/data').inc()
    if random.choice([True, False]):
        SUCCESS_COUNT.inc()
        return jsonify({"data": [1, 2, 3, 4]})
    else:
        ERROR_COUNT.inc()
        return jsonify({"error": "Something went wrong"}), 500

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    start_http_server(8000)  # Expose metrics on port 8000
    app.run(host='0.0.0.0', port=5000)
