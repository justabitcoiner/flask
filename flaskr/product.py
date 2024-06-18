from flask import Blueprint, flash, g, redirect, render_template, request, url_for, render_template
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint("product", __name__, url_prefix="/products")


@bp.route("/")
def index():
    db = get_db()
    products = db.execute("SELECT id, title, created FROM product ORDER BY created DESC").fetchall()
    return render_template("product/index.html", products=products)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute("INSERT INTO product (title) VALUES (?)", (title,))
            db.commit()
            return redirect(url_for("product.index"))

    return render_template("product/create.html")


def get_product(id, check_author=True):
    product = (
        get_db()
        .execute(
            "SELECT id, title, created" " FROM product" " WHERE id = ?",
            (id,),
        )
        .fetchone()
    )

    if product is None:
        abort(404, f"Product id {id} doesn't exist.")

    # if check_author and product["author_id"] != g.user["id"]:
    #     abort(403)

    return product


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    product = get_product(id)

    if request.method == "POST":
        title = request.form["title"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute("UPDATE product SET title = ?" " WHERE id = ?", (title, id))
            db.commit()
            return redirect(url_for("product.index"))

    return render_template("product/update.html", product=product)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    get_product(id)
    db = get_db()
    db.execute("DELETE FROM product WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("product.index"))
