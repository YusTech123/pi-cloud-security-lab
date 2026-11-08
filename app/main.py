import os
import logging

import psycopg
from psycopg.rows import dict_row
from flask import Flask, jsonify

app = Flask(__name__)


def get_db_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "5433")),
        dbname=os.getenv("DB_NAME", "customerdb"),
        user=os.getenv("DB_USER", "customer_api"),
        password=os.environ["DB_PASSWORD"],
        connect_timeout=5,
        row_factory=dict_row
    )


@app.get("/")
def index():
    return jsonify({
        "message": "DevSecOps Customer API",
        "version": "1.0"
    }), 200


@app.get("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "customer-api"
    }), 200


@app.get("/customers")
def get_customers():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id, name, email "
                    "FROM public.customers ORDER BY id"
                )
                customers = cursor.fetchall()

        return jsonify(customers), 200

    except psycopg.Error:
        app.logger.exception("Database query failed")
        return jsonify({"error": "Database unavailable"}), 503


@app.get("/customers/<int:customer_id>")
def get_customer(customer_id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id, name, email "
                    "FROM public.customers WHERE id = %s",
                    (customer_id,)
                )
                customer = cursor.fetchone()

        if customer is None:
            return jsonify({"error": "Customer not found"}), 404

        return jsonify(customer), 200

    except psycopg.Error:
        app.logger.exception("Database query failed")
        return jsonify({"error": "Database unavailable"}), 503


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)

