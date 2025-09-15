import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("psql 'postgresql://neondb_owner:npg_wE3ISfV6yXeU@ep-bitter-hill-ad9pb0m3-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'!")

# Connect to Neon
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Initialize table if it doesn't exist
def init_db():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
            psql 'postgresql://neondb_owner:npg_wE3ISfV6yXeU@ep-bitter-hill-ad9pb0m3-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')
            );
            """)
            conn.commit()
    finally:
        conn.close()

@app.route("/api/items", methods=["GET"])
def list_items():
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM items ORDER BY id DESC;")
            rows = cur.fetchall()
            return jsonify(rows)
    finally:
        conn.close()

@app.route("/api/items", methods=["POST"])
def create_item():
    data = request.get_json() or {}
    name = data.get("name")
    value = data.get("value")
    if not name or value is None:
        return jsonify({"error": "name and value required"}), 400

    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
            DATABASE_URL, psql 'postgresql://neondb_owner:npg_wE3ISfV6yXeU@ep-bitter-hill-ad9pb0m3-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')
            )
            item = cur.fetchone()
            conn.commit()
            return jsonify(item), 201
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
