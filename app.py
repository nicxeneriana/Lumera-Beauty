import os
import pymysql
from pymysql.cursors import DictCursor
from functools import wraps
from datetime import datetime

from flask import (
    Flask, render_template, request, redirect, url_for,
    session, flash, g, abort
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAGE_SIZE = 8

app = Flask(__name__)
app.config["SECRET_KEY"] = "lumera-secret-key-123"
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------
def get_db():
    if "db" not in g:
        g.db = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="lumera_beauty",
            charset="utf8mb4",
            cursorclass=DictCursor,
            autocommit=False
        )
    return g.db


@app.teardown_appcontext
def close_db(error):
    db = g.pop("db", None)

    if db is not None:
        try:
            db.close()
        except:
            pass


def query_db(sql, params=None, one=False):
    """Jalankan SELECT dan kembalikan list of dict (atau satu dict jika one=True)."""
    db = get_db()
    with db.cursor() as cur:
        cur.execute(sql, params or [])
        rows = cur.fetchall()
    if one:
        return rows[0] if rows else None
    return rows


def execute_db(sql, params=None):
    """Jalankan INSERT/UPDATE/DELETE. Mengembalikan lastrowid (untuk INSERT)."""
    db = get_db()
    with db.cursor() as cur:
        cur.execute(sql, params or [])
        return cur.lastrowid


def init_db_if_needed():
    # Dengan MySQL/phpMyAdmin, database & tabel harus sudah dibuat lebih dulu
    # (misalnya dengan mengimpor file .sql lewat phpMyAdmin). Tidak ada lagi
    # pembuatan otomatis seperti pada file SQLite.
    pass


def format_rupiah(value):
    try:
        return "Rp {:,.0f}".format(value).replace(",", ".")
    except (ValueError, TypeError):
        return value


app.jinja_env.filters["rupiah"] = format_rupiah


# ---------------------------------------------------------------------------
# Auth helpers
# ---------------------------------------------------------------------------
def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("admin_id"):
            return redirect(url_for("admin_login", next=request.path))
        return f(*args, **kwargs)
    return wrapper


@app.context_processor
def inject_globals():
    categories = query_db("SELECT * FROM categories ORDER BY name")
    brands = query_db("SELECT * FROM brands ORDER BY name")
    return dict(
        nav_categories=categories,
        nav_brands=brands,
        admin_name=session.get("admin_name"),
    )


# ---------------------------------------------------------------------------
# Public storefront
# ---------------------------------------------------------------------------
@app.route("/")
def index():

    keyword = request.args.get("q", "").strip()

    if keyword:
        latest = query_db("""
            SELECT p.*, b.name AS brand_name
            FROM products p
            JOIN brands b ON b.id = p.brand_id
            LEFT JOIN categories c ON c.id = p.category_id
            WHERE
                p.name LIKE %s
                OR b.name LIKE %s
                OR c.name LIKE %s
            ORDER BY p.name
        """, (
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%"
        ))

    else:
        latest = query_db("""
            SELECT p.*, b.name AS brand_name
            FROM products p
            JOIN brands b ON b.id = p.brand_id
            ORDER BY p.created_at DESC, p.id DESC
            LIMIT 4
        """)

    return render_template("index.html", products=latest)

@app.route("/produk")
def products():
    category = request.args.get("kategori", "")
    keyword = request.args.get("q", "").strip()
    selected_brands = request.args.getlist("merek")
    harga_min = request.args.get("harga_min", type=int)
    harga_max = request.args.get("harga_max", type=int)
    urutkan = request.args.get("urutkan", "terbaru")
    page = request.args.get("page", 1, type=int)
    if page < 1:
        page = 1

    where = []
    params = []

    if category and category != "semua":
        where.append("c.name = %s")
        params.append(category)

    if keyword:
        where.append("""
            (
                p.name LIKE %s OR
                b.name LIKE %s OR
                c.name LIKE %s
            )
        """)
        like = f"%{keyword}%"
        params.extend([like, like, like])

    if selected_brands:
        placeholders = ",".join(["%s"] * len(selected_brands))
        where.append(f"b.name IN ({placeholders})")
        params.extend(selected_brands)

    if harga_min is not None:
        where.append("p.price >= %s")
        params.append(harga_min)
    if harga_max is not None:
        where.append("p.price <= %s")
        params.append(harga_max)

    where_sql = ("WHERE " + " AND ".join(where)) if where else ""

    order_sql = "p.created_at DESC, p.id DESC"
    if urutkan == "harga_asc":
        order_sql = "p.price ASC"
    elif urutkan == "harga_desc":
        order_sql = "p.price DESC"
    elif urutkan == "nama":
        order_sql = "p.name ASC"

    count_sql = f"""SELECT COUNT(*) AS total FROM products p
                     JOIN brands b ON b.id = p.brand_id
                     JOIN categories c ON c.id = p.category_id
                     {where_sql}"""
    total = query_db(count_sql, params, one=True)["total"]
    total_pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
    page = min(page, total_pages)
    offset = (page - 1) * PAGE_SIZE

    list_sql = f"""SELECT p.*, b.name AS brand_name, c.name AS category_name
                    FROM products p
                    JOIN brands b ON b.id = p.brand_id
                    JOIN categories c ON c.id = p.category_id
                    {where_sql}
                    ORDER BY {order_sql}
                    LIMIT %s OFFSET %s"""
    items = query_db(list_sql, params + [PAGE_SIZE, offset])

    return render_template(
        "products.html",
        products=items,
        total=total,
        page=page,
        total_pages=total_pages,
        page_size=PAGE_SIZE,
        selected_category=category or "semua",
        selected_brands=selected_brands,
        harga_min=harga_min,
        harga_max=harga_max,
        urutkan=urutkan,
        q=keyword,
    )


@app.route("/produk/<int:product_id>")
def product_detail(product_id):
    product = query_db(
        """SELECT p.*, b.name AS brand_name, c.name AS category_name
           FROM products p
           JOIN brands b ON b.id = p.brand_id
           JOIN categories c ON c.id = p.category_id
           WHERE p.id = %s""",
        (product_id,),
        one=True,
    )
    if product is None:
        abort(404)

    related = query_db(
        """SELECT p.*, b.name AS brand_name
           FROM products p JOIN brands b ON b.id = p.brand_id
           WHERE p.category_id = %s AND p.id != %s
           ORDER BY p.created_at DESC LIMIT 4""",
        (product["category_id"], product_id),
    )

    return render_template("product_detail.html", product=product, related=related)


# ---------------------------------------------------------------------------
# Admin auth
# ---------------------------------------------------------------------------
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if session.get("admin_id"):
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        user = query_db(
            "SELECT * FROM admin_users WHERE email = %s", (email,), one=True
        )
        if user and check_password_hash(user["password_hash"], password):
            session["admin_id"] = user["id"]
            session["admin_name"] = user["name"]
            next_url = request.args.get("next") or url_for("admin_dashboard")
            return redirect(next_url)
        flash("Email atau password salah.", "error")

    return render_template("admin/login.html")


@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("admin_login"))


# ---------------------------------------------------------------------------
# Admin dashboard
# ---------------------------------------------------------------------------
@app.route("/admin")
@admin_required
def admin_root():
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    total_produk = query_db("SELECT COUNT(*) AS total FROM products", one=True)["total"]
    stok_tersedia = query_db(
        "SELECT COUNT(*) AS total FROM products WHERE stock > 0", one=True
    )["total"]
    stok_habis = query_db(
        "SELECT COUNT(*) AS total FROM products WHERE stock = 0", one=True
    )["total"]
    total_transaksi = query_db(
        "SELECT COUNT(*) AS total FROM stock_movements", one=True
    )["total"]

    chart_rows = query_db(
        """SELECT SUBSTR(created_at, 1, 10) AS d, SUM(quantity) AS total
           FROM stock_movements
           WHERE type = 'keluar'
           GROUP BY d ORDER BY d DESC LIMIT 7"""
    )
    chart_labels = [r["d"] for r in reversed(chart_rows)]
    chart_values = [r["total"] for r in reversed(chart_rows)]

    terlaris = query_db(
        """SELECT p.name, SUM(sm.quantity) AS total_keluar
           FROM stock_movements sm JOIN products p ON p.id = sm.product_id
           WHERE sm.type = 'keluar'
           GROUP BY sm.product_id ORDER BY total_keluar DESC LIMIT 3"""
    )
    hampir_habis = query_db(
        "SELECT name, stock FROM products WHERE stock > 0 ORDER BY stock ASC LIMIT 5"
    )

    return render_template(
        "admin/dashboard.html",
        total_produk=total_produk,
        stok_tersedia=stok_tersedia,
        stok_habis=stok_habis,
        total_transaksi=total_transaksi,
        chart_labels=chart_labels,
        chart_values=chart_values,
        terlaris=terlaris,
        hampir_habis=hampir_habis,
    )


# ---------------------------------------------------------------------------
# Admin: produk CRUD
# ---------------------------------------------------------------------------
@app.route("/admin/produk")
@admin_required
def admin_products():
    q = request.args.get("q", "").strip()
    sql = """SELECT p.*, b.name AS brand_name, c.name AS category_name
              FROM products p
              JOIN brands b ON b.id = p.brand_id
              JOIN categories c ON c.id = p.category_id"""
    params = []
    if q:
        sql += " WHERE p.name LIKE %s"
        params.append(f"%{q}%")
    sql += " ORDER BY p.id DESC"
    items = query_db(sql, params)
    return render_template("admin/products.html", products=items, q=q)

@app.route("/admin/produk/tambah", methods=["GET", "POST"])
@admin_required
def admin_product_add():
    categories = query_db("SELECT * FROM categories ORDER BY name")
    brands = query_db("SELECT * FROM brands ORDER BY name")

    if request.method == "POST":
        form = request.form
        image = request.files.get("image")
        filename = ""

        if image and image.filename:
            filename = secure_filename(image.filename)
            image.save(
                os.path.join(app.config["UPLOAD_FOLDER"], filename)
            )

        execute_db(
            """
            INSERT INTO products
            (name, brand_id, category_id, price, stock, volume,
             description, image_color, image_icon, image, is_new)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                form["name"].strip(),
                form["brand_id"],
                form["category_id"],
                int(form["price"]),
                int(form.get("stock") or 0),
                form.get("volume", "").strip(),
                form.get("description", "").strip(),
                form.get("image_color", "#F3C6D3"),
                form.get("image_icon", "serum"),
                filename,
                1 if form.get("is_new") == "on" else 0,
            ),
        )

        get_db().commit()
        flash("Produk berhasil ditambahkan.", "success")
        return redirect(url_for("admin_products"))

    return render_template(
        "admin/product_form.html",
        categories=categories,
        brands=brands,
        product=None,
    )
@app.route("/admin/produk/edit/<int:product_id>", methods=["GET", "POST"])
@admin_required
def admin_product_edit(product_id):
    product = query_db(
        "SELECT * FROM products WHERE id = %s", (product_id,), one=True
    )
    if product is None:
        abort(404)
    categories = query_db("SELECT * FROM categories ORDER BY name")
    brands = query_db("SELECT * FROM brands ORDER BY name")

    if request.method == "POST":
        form = request.form
        filename = product["image"]

        image = request.files.get("image")

        if image and image.filename:
            filename = secure_filename(image.filename)
            image.save(
                os.path.join(app.config["UPLOAD_FOLDER"], filename)
            )
        execute_db(
            """UPDATE products SET
               name=%s, brand_id=%s, category_id=%s, price=%s, stock=%s, volume=%s,
               description=%s, image_color=%s, image_icon=%s, image=%s, is_new=%s
               WHERE id = %s""",
            (
                form["name"].strip(),
                form["brand_id"],
                form["category_id"],
                int(form["price"]),
                int(form.get("stock") or 0),
                form.get("volume", "").strip(),
                form.get("description", "").strip(),
                form.get("image_color", "#F3C6D3"),
                form.get("image_icon", "serum"),
                filename,
                1 if form.get("is_new") == "on" else 0,
                product_id,
            ),
        )
        get_db().commit()
        flash("Produk berhasil diperbarui.", "success")
        return redirect(url_for("admin_products"))

    return render_template(
        "admin/product_form.html", categories=categories, brands=brands, product=product
    )


@app.route("/admin/produk/hapus/<int:product_id>", methods=["POST"])
@admin_required
def admin_product_delete(product_id):
    execute_db("DELETE FROM stock_movements WHERE product_id = %s", (product_id,))
    execute_db("DELETE FROM products WHERE id = %s", (product_id,))
    get_db().commit()
    flash("Produk berhasil dihapus.", "success")
    return redirect(url_for("admin_products"))


# ---------------------------------------------------------------------------
# Admin: kategori & merek
# ---------------------------------------------------------------------------
@app.route("/admin/kategori", methods=["GET", "POST"])
@admin_required
def admin_categories():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if name:
            try:
                execute_db("INSERT INTO categories (name) VALUES (%s)", (name,))
                get_db().commit()
                flash("Kategori ditambahkan.", "success")
            except pymysql.err.IntegrityError:
                flash("Kategori sudah ada.", "error")
        return redirect(url_for("admin_categories"))
    items = query_db(
        """SELECT c.*, (SELECT COUNT(*) FROM products p WHERE p.category_id = c.id) AS total
           FROM categories c ORDER BY c.name"""
    )
    return render_template("admin/categories.html", categories=items)


@app.route("/admin/kategori/hapus/<int:cat_id>", methods=["POST"])
@admin_required
def admin_category_delete(cat_id):
    in_use = query_db(
        "SELECT COUNT(*) AS total FROM products WHERE category_id = %s", (cat_id,), one=True
    )["total"]
    if in_use:
        flash("Kategori masih digunakan oleh produk.", "error")
    else:
        execute_db("DELETE FROM categories WHERE id = %s", (cat_id,))
        get_db().commit()
        flash("Kategori dihapus.", "success")
    return redirect(url_for("admin_categories"))


@app.route("/admin/merek", methods=["GET", "POST"])
@admin_required
def admin_brands():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if name:
            try:
                execute_db("INSERT INTO brands (name) VALUES (%s)", (name,))
                get_db().commit()
                flash("Merek ditambahkan.", "success")
            except pymysql.err.IntegrityError:
                flash("Merek sudah ada.", "error")
        return redirect(url_for("admin_brands"))
    items = query_db(
        """SELECT b.*, (SELECT COUNT(*) FROM products p WHERE p.brand_id = b.id) AS total
           FROM brands b ORDER BY b.name"""
    )
    return render_template("admin/brands.html", brands=items)


@app.route("/admin/merek/hapus/<int:brand_id>", methods=["POST"])
@admin_required
def admin_brand_delete(brand_id):
    in_use = query_db(
        "SELECT COUNT(*) AS total FROM products WHERE brand_id = %s", (brand_id,), one=True
    )["total"]
    if in_use:
        flash("Merek masih digunakan oleh produk.", "error")
    else:
        execute_db("DELETE FROM brands WHERE id = %s", (brand_id,))
        get_db().commit()
        flash("Merek dihapus.", "success")
    return redirect(url_for("admin_brands"))


# ---------------------------------------------------------------------------
# Admin: stok
# ---------------------------------------------------------------------------
@app.route("/admin/stok")
@admin_required
def admin_stock():
    tab = request.args.get("tab", "masuk")
    if tab not in ("masuk", "keluar", "riwayat"):
        tab = "masuk"

    if tab == "riwayat":
        rows = query_db(
            """SELECT sm.*, p.name AS product_name
               FROM stock_movements sm JOIN products p ON p.id = sm.product_id
               ORDER BY sm.created_at DESC, sm.id DESC"""
        )
    else:
        rows = query_db(
            """SELECT sm.*, p.name AS product_name
               FROM stock_movements sm JOIN products p ON p.id = sm.product_id
               WHERE sm.type = %s
               ORDER BY sm.created_at DESC, sm.id DESC""",
            (tab,),
        )

    products_list = query_db("SELECT id, name, stock FROM products ORDER BY name")
    return render_template("admin/stock.html", rows=rows, tab=tab, products=products_list)


@app.route("/admin/stok/tambah", methods=["POST"])
@admin_required
def admin_stock_add():
    product_id = int(request.form["product_id"])
    movement_type = request.form["type"]
    quantity = int(request.form["quantity"])
    note = request.form.get("note", "").strip()

    if movement_type not in ("masuk", "keluar"):
        abort(400)

    product = query_db("SELECT * FROM products WHERE id = %s", (product_id,), one=True)
    if product is None:
        abort(404)

    if movement_type == "keluar" and quantity > product["stock"]:
        flash("Jumlah stok keluar melebihi stok yang tersedia.", "error")
        return redirect(url_for("admin_stock", tab=movement_type))

    execute_db(
        "INSERT INTO stock_movements (product_id, type, quantity, note) VALUES (%s, %s, %s, %s)",
        (product_id, movement_type, quantity, note),
    )
    delta = quantity if movement_type == "masuk" else -quantity
    execute_db("UPDATE products SET stock = stock + %s WHERE id = %s", (delta, product_id))
    get_db().commit()
    flash("Stok berhasil diperbarui.", "success")
    return redirect(url_for("admin_stock", tab=movement_type))


# ---------------------------------------------------------------------------
# Admin: transaksi (ringkasan stok keluar) & laporan
# ---------------------------------------------------------------------------
@app.route("/admin/transactions")
@admin_required
def admin_transactions():

    db = get_db()
    cursor = db.cursor()

    # Ambil semua transaksi
    cursor.execute("""
        SELECT *
        FROM transactions
        ORDER BY created_at DESC
    """)
    rows = cursor.fetchall()

    # Total pendapatan
    total_income = sum(r["total"] for r in rows)

    # Hitung transaksi hari ini
    from datetime import date

    today = date.today()

    today_count = sum(
        1 for row in rows
        if row["created_at"].date() == today
    )

    return render_template(
        "admin/transactions.html",
        rows=rows,
        total_income=total_income,
        today_count=today_count
    )

@app.route("/admin/laporan")
@admin_required
def admin_reports():
    per_kategori = query_db(
        """SELECT c.name, COUNT(p.id) AS total_produk, COALESCE(SUM(p.stock),0) AS total_stok
           FROM categories c LEFT JOIN products p ON p.category_id = c.id
           GROUP BY c.id ORDER BY c.name"""
    )
    per_brand = query_db(
        """SELECT b.name, COUNT(p.id) AS total_produk, COALESCE(SUM(p.stock),0) AS total_stok
           FROM brands b LEFT JOIN products p ON p.brand_id = b.id
           GROUP BY b.id ORDER BY b.name"""
    )
    nilai_inventori = query_db(
        "SELECT COALESCE(SUM(price * stock), 0) AS total FROM products", one=True
    )["total"]
    return render_template(
        "admin/reports.html",
        per_kategori=per_kategori,
        per_brand=per_brand,
        nilai_inventori=nilai_inventori,
    )
from datetime import datetime
from flask import flash, redirect, url_for

@app.route("/admin/transactions/add", methods=["GET", "POST"])
@admin_required
def admin_transaction_add():

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT id, name, price, stock
        FROM products
        ORDER BY name
    """)
    products = cursor.fetchall()

    if request.method == "POST":

        product_ids = request.form.getlist("product_id[]")
        qtys = request.form.getlist("qty[]")

        customer = request.form.get("customer_name") or "Umum"
        payment = request.form["payment_method"]

        invoice = "INV" + datetime.now().strftime("%Y%m%d%H%M%S")

        total = 0
        items = []

        # Validasi stok dan hitung total
        for pid, qty in zip(product_ids, qtys):

            pid = int(pid)
            qty = int(qty)

            cursor.execute("""
                SELECT *
                FROM products
                WHERE id=%s
            """, (pid,))
            product = cursor.fetchone()

            if not product:
                flash("Produk tidak ditemukan.", "error")
                return redirect(url_for("admin_transaction_add"))

            if qty > product["stock"]:
                flash(f"Stok {product['name']} tidak mencukupi.", "error")
                return redirect(url_for("admin_transaction_add"))

            subtotal = product["price"] * qty
            total += subtotal

            items.append({
                "product_id": pid,
                "qty": qty,
                "price": product["price"],
                "subtotal": subtotal
            })

        # Simpan transaksi
        cursor.execute("""
            INSERT INTO transactions
            (invoice, customer_name, total, payment_method)
            VALUES (%s,%s,%s,%s)
        """, (
            invoice,
            customer,
            total,
            payment
        ))

        transaction_id = cursor.lastrowid

        # Simpan detail transaksi dan kurangi stok
        for item in items:

            cursor.execute("""
                INSERT INTO transaction_items
                (transaction_id, product_id, qty, price, subtotal)
                VALUES (%s,%s,%s,%s,%s)
            """, (
                transaction_id,
                item["product_id"],
                item["qty"],
                item["price"],
                item["subtotal"]
            ))

            cursor.execute("""
                UPDATE products
                SET stock = stock - %s
                WHERE id=%s
            """, (
                item["qty"],
                item["product_id"]
            ))

            cursor.execute("""
                INSERT INTO stock_movements
                (product_id, type, quantity, note)
                VALUES (%s,%s,%s,%s)
            """, (
                item["product_id"],
                "keluar",
                item["qty"],
                "Penjualan " + invoice
            ))

        db.commit()

        flash("Transaksi berhasil disimpan.", "success")
        return redirect(url_for("admin_transactions"))

    return render_template(
        "admin/transaction_form.html",
        products=products
    )
@app.route("/admin/transactions/<int:transaction_id>")
@admin_required
def admin_transaction_detail(transaction_id):

    db = get_db()
    cursor = db.cursor()

    print("ID =", transaction_id)

    cursor.execute("""
        SELECT *
        FROM transactions
        WHERE id=%s
    """, (transaction_id,))

    transaction = cursor.fetchone()

    print("Transaction =", transaction)

    if transaction is None:
        return "Transaksi tidak ditemukan"

    cursor.execute("""
        SELECT
            ti.*,
            p.name AS product_name
        FROM transaction_items ti
        JOIN products p
            ON p.id = ti.product_id
        WHERE ti.transaction_id=%s
    """, (transaction_id,))

    items = cursor.fetchall()

    return render_template(
        "admin/transaction_detail.html",
        transaction=transaction,
        items=items
    )
@app.route("/admin/transaksi/delete/<int:transaction_id>", methods=["POST"])
@admin_required
def admin_transaction_delete(transaction_id):

    db = get_db()
    cursor = db.cursor()

    # Ambil item transaksi terlebih dahulu
    cursor.execute("""
        SELECT product_id, qty
        FROM transaction_items
        WHERE transaction_id = %s
    """, (transaction_id,))

    items = cursor.fetchall()

    # Kembalikan stok produk
    for item in items:
        cursor.execute("""
            UPDATE products
            SET stock = stock + %s
            WHERE id = %s
        """, (
            item["qty"],
            item["product_id"]
        ))

    # Hapus detail transaksi
    cursor.execute("""
        DELETE FROM transaction_items
        WHERE transaction_id = %s
    """, (transaction_id,))


    # Hapus transaksi utama
    cursor.execute("""
        DELETE FROM transactions
        WHERE id = %s
    """, (transaction_id,))


    db.commit()

    cursor.close()
    db.close()

    return redirect(url_for("admin_transactions"))  


@app.route("/admin/pengaturan", methods=["GET", "POST"])
@admin_required
def admin_settings():
    user = query_db(
        "SELECT * FROM admin_users WHERE id = %s", (session["admin_id"],), one=True
    )

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        new_password = request.form.get("new_password", "")
        execute_db("UPDATE admin_users SET name = %s WHERE id = %s", (name, user["id"]))
        if new_password:
            execute_db(
                "UPDATE admin_users SET password_hash = %s WHERE id = %s",
                (generate_password_hash(new_password), user["id"]),
            )
        get_db().commit()
        session["admin_name"] = name
        flash("Pengaturan berhasil disimpan.", "success")
        return redirect(url_for("admin_settings"))

    return render_template("admin/settings.html", user=user)


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
