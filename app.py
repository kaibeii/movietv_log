from flask import Flask, render_template, request, redirect, url_for, flash
from database import (
    init_db,
    add_entry,
    get_all_entries,
    search_entries,
    get_entry_by_id,
    get_distinct_genres,
    update_entry,
    delete_entry,
)

GENRES = [
    "Action", "Adventure", "Animation", "Comedy", "Crime",
    "Documentary", "Drama", "Fantasy", "Horror", "Musical",
    "Mystery", "Romance", "Sci-Fi", "Thriller", "Western",
]

app = Flask(__name__, template_folder="page")
app.secret_key = "movie-log-secret-key"


# ── Home / List ───────────────────────────────────────────────────────────────

@app.route("/")
def index():
    sort_by = request.args.get("sort_by", "date_watched")
    order   = request.args.get("order", "DESC")
    entries = get_all_entries(sort_by=sort_by, order=order)
    genres  = get_distinct_genres()
    return render_template("index.html", entries=entries, genres=genres,
                           sort_by=sort_by, order=order)


# ── Search / Filter ───────────────────────────────────────────────────────────

@app.route("/search")
def search():
    query       = request.args.get("q", "")
    genre       = request.args.get("genre", "")
    type_filter = request.args.get("type", "")
    min_rating  = request.args.get("min_rating", 1, type=int)
    entries     = search_entries(query, genre, type_filter, min_rating)
    genres      = get_distinct_genres()
    return render_template("search.html", entries=entries, genres=genres,
                           q=query, genre=genre, type_filter=type_filter,
                           min_rating=min_rating)


# ── Add ───────────────────────────────────────────────────────────────────────

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title        = request.form["title"].strip()
        type_        = request.form["type"]
        genre        = ", ".join(request.form.getlist("genre"))
        rating       = request.form.get("rating", type=int)
        date_watched = request.form["date_watched"]
        notes        = request.form["notes"].strip()

        if not title:
            flash("Title is required.", "error")
            return redirect(url_for("add"))

        add_entry(title, type_, genre, rating, date_watched, notes)
        flash(f'"{title}" added to your log!', "success")
        return redirect(url_for("index"))

    return render_template("add.html", genres=GENRES)


# ── Edit ──────────────────────────────────────────────────────────────────────

@app.route("/edit/<int:entry_id>", methods=["GET", "POST"])
def edit(entry_id):
    entry = get_entry_by_id(entry_id)
    if entry is None:
        flash("Entry not found.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        title        = request.form["title"].strip()
        type_        = request.form["type"]
        genre        = ", ".join(request.form.getlist("genre"))
        rating       = request.form.get("rating", type=int)
        date_watched = request.form["date_watched"]
        notes        = request.form["notes"].strip()

        update_entry(entry_id, title, type_, genre, rating, date_watched, notes)
        flash(f'"{title}" updated.', "success")
        return redirect(url_for("index"))

    return render_template("edit.html", entry=entry, genres=GENRES)


# ── Delete ────────────────────────────────────────────────────────────────────

@app.route("/delete/<int:entry_id>", methods=["POST"])
def delete(entry_id):
    entry = get_entry_by_id(entry_id)
    if entry:
        delete_entry(entry_id)
        flash(f'"{entry["title"]}" removed from your log.', "success")
    else:
        flash("Entry not found.", "error")
    return redirect(url_for("index"))


# ── Entry ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    app.run(debug=True)