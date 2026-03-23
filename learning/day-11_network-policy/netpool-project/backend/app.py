# backend/app.py
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2          # for PostgreSQL
# import mysql.connector  # uncomment for MySQL

app = Flask(__name__)
CORS(app)

def get_pg_conn():
    return psycopg2.connect(
        host=os.environ["DB_HOST"], # postgres-svc.database.svc.cluster.local
        port=os.environ.get("DB_PORT", 5432),
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )

# For MySQL swap get_pg_conn() with:
# def get_mysql_conn():
#     return mysql.connector.connect(
#         host=os.environ["DB_HOST"],      # mysql-svc.database.svc.cluster.local
#         port=int(os.environ.get("DB_PORT", 3306)),
#         database=os.environ["DB_NAME"],
#         user=os.environ["DB_USER"],
#         password=os.environ["DB_PASSWORD"],
#     )

def init_db():
    """Create items table on startup"""
    conn = get_pg_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

# ─── CRUD routes ─────────────────────────────────────────────
@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/items", methods=["GET"])
def get_items():
    conn = get_pg_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, description, created_at FROM items ORDER BY id")
    rows = cur.fetchall()
    cur.close(); conn.close()
    return jsonify([
        {"id": r[0], "name": r[1], "description": r[2], "created_at": str(r[3])}
        for r in rows
    ])

@app.route("/items", methods=["POST"])
def create_item():
    data = request.json
    conn = get_pg_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO items (name, description) VALUES (%s, %s) RETURNING id",
        (data["name"], data.get("description", ""))
    )
    new_id = cur.fetchone()[0]
    conn.commit(); cur.close(); conn.close()
    return jsonify({"id": new_id, "message": "created"}), 201

@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    data = request.json
    conn = get_pg_conn()
    cur = conn.cursor()
    cur.execute(
        "UPDATE items SET name=%s, description=%s WHERE id=%s",
        (data["name"], data.get("description", ""), item_id)
    )
    conn.commit(); cur.close(); conn.close()
    return jsonify({"message": "updated"})

@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    conn = get_pg_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM items WHERE id=%s", (item_id,))
    conn.commit(); cur.close(); conn.close()
    return jsonify({"message": "deleted"})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)