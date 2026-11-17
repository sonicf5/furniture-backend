import sqlite3
import json
from flask import Flask, jsonify, send_from_directory

app = Flask(__name__)


# ===== 1. Создать базу и добавить товары (один раз при запуске) =====
def setup_database():
    conn = sqlite3.connect("products.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL,
            type TEXT,
            material TEXT,
            description TEXT,
            image_url TEXT,
            model_url TEXT
        )
    """)

    # Если товаров ещё нет — добавим 6 штук
    count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    if count == 0:
        conn.executemany(
            "INSERT INTO products (name, price, type, material, description, image_url, model_url) VALUES (?, ?, ?, ?, ?, ?, ?)",
            [
                ("Стул Nord", 5490, "Стул", "Дерево", "Скандинавский стул из дуба", "/images/chair-nord.jpg", "/models/chair-nord.glb"),
                ("Стул Loft", 3990, "Стул", "Металл", "Стул в стиле лофт", "/images/chair-loft.jpg", "/models/chair-loft.glb"),
                ("Стол Oak Line", 24990, "Стол", "Дерево", "Обеденный стол из массива дуба", "/images/table-oak.jpg", "/models/table-oak.glb"),
                ("Стол Glass Pro", 18990, "Стол", "Металл", "Стол со стеклом и алюминиевым каркасом", "/images/table-glass.jpg", "/models/table-glass.glb"),
                ("Шкаф Classic", 32990, "Шкаф", "ЛДСП", "Трёхдверный шкаф из ЛДСП", "/images/wardrobe-classic.jpg", "/models/wardrobe-classic.glb"),
                ("Шкаф Loft Industrial", 41990, "Шкаф", "Металл", "Шкаф с металлическим каркасом", "/images/wardrobe-loft.jpg", "/models/wardrobe-loft.glb"),
            ]
        )
        conn.commit()
        print("✅ База создана, добавлено 6 товаров")

    conn.close()


# ===== 2. Два главных запроса API =====

@app.route("/api/products")
def all_products():
    """Список всех товаров"""
    conn = sqlite3.connect("products.db")
    rows = conn.execute("SELECT * FROM products").fetchall()
    conn.close()

    # Превращаем строки БД в список словарей
    products = []
    for row in rows:
        products.append({
            "id": row[0],
            "name": row[1],
            "price": row[2],
            "type": row[3],
            "material": row[4],
            "description": row[5],
            "image_url": row[6],
            "model_url": row[7],
        })
    return jsonify(products)


@app.route("/api/products/<int:product_id>")
def one_product(product_id):
    """Один товар по id"""
    conn = sqlite3.connect("products.db")
    row = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    conn.close()

    if row is None:
        return jsonify({"error": "Product not found"}), 404

    return jsonify({
        "id": row[0],
        "name": row[1],
        "price": row[2],
        "type": row[3],
        "material": row[4],
        "description": row[5],
        "image_url": row[6],
        "model_url": row[7],
    })


# ===== 3. Отдаём файлы из папки public/ =====

@app.route("/models/<filename>")
def model_file(filename):
    return send_from_directory("public/models", filename)


@app.route("/images/<filename>")
def image_file(filename):
    return send_from_directory("public/images", filename)


# ===== 4. Запуск =====
setup_database()
    #app.run(port=3000, debug=True)
