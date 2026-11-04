from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "customer-api"
    }), 200


@app.get("/")
def index():
    return jsonify({
        "message": "DevSecOps Customer API",
        "version": "1.0"
    }), 200
# Temporary test data
# We'll replace this with PostgreSQL later.
customers = [
    {"id": 1, "name": "Test Customer One"},
    {"id": 2, "name": "Test Customer Two"}
]


@app.get("/customers")
def get_customers():
    return jsonify(customers), 200


@app.get("/customers/<int:customer_id>")
def get_customer(customer_id):
    customer = next(
        (c for c in customers if c["id"] == customer_id),
        None
    )

    if customer is None:
        return jsonify({"error": "Customer not found"}), 404

    return jsonify(customer), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
