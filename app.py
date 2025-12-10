import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

DB_PATH = "golf.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT,
            model TEXT,
            club_type TEXT,
            condition TEXT,
            loft TEXT,
            shaft TEXT,
            flex TEXT,
            title TEXT,
            base_price INTEGER,
            min_price INTEGER,
            stock INTEGER,
            description TEXT,
            channel_naver INTEGER,
            channel_coupang INTEGER,
            channel_own INTEGER,
            created_at TEXT
        )
        """
    )
    conn.commit()
    conn.close()


@app.route("/")
def shop():
    """고객용 상품 리스트 페이지"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, brand, model, club_type, condition, title, base_price, description, created_at
        FROM products
        ORDER BY id DESC
        """
    )
    rows = cur.fetchall()
    conn.close()

    products = []
    for row in rows:
        products.append(
            {
                "id": row[0],
                "brand": row[1],
                "model": row[2],
                "club_type": row[3],
                "condition": row[4],
                "title": row[5],
                "base_price": row[6],
                "description": row[7],
                "created_at": row[8],
            }
        )

    return render_template("shop.html", products=products)


@app.route("/admin")
def admin():
    """관리자 상품 등록 페이지"""
    return render_template("admin.html")


@app.route("/api/products", methods=["POST"])
def api_create_product():
    """관리자 페이지에서 상품 등록할 때 호출되는 API"""
    data = request.get_json(force=True)

    brand = data.get("brand") or ""
    model = data.get("model") or ""
    club_type = data.get("clubType") or ""
    condition = data.get("condition") or ""
    loft = data.get("loft") or ""
    shaft = data.get("shaft") or ""
    flex = data.get("flex") or ""
    title = data.get("title") or ""
    base_price = int(data.get("basePrice") or 0)
    min_price = int(data.get("minPrice") or 0)
    stock = int(data.get("stock") or 1)
    description = data.get("description") or ""
    ch_naver = 1 if data.get("channels", {}).get("naver") else 0
    ch_coupang = 1 if data.get("channels", {}).get("coupang") else 0
    ch_own = 1 if data.get("channels", {}).get("own") else 0

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO products (
            brand, model, club_type, condition, loft, shaft, flex,
            title, base_price, min_price, stock, description,
            channel_naver, channel_coupang, channel_own, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            brand,
            model,
            club_type,
            condition,
            loft,
            shaft,
            flex,
            title,
            base_price,
            min_price,
            stock,
            description,
            ch_naver,
            ch_coupang,
            ch_own,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )
    conn.commit()
    conn.close()

    return jsonify({"ok": True})


import os

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
