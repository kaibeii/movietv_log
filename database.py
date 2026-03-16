import sqlite3

DB_NAME = "movie_log.db"


def get_connection():
    """Return a database connection with row_factory set for dict-like access."""
    con = sqlite3.connect(DB_NAME)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    """Create the watched table if it doesn't already exist."""
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS watched (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT    NOT NULL,
            type        TEXT    NOT NULL CHECK(type IN ('Movie', 'TV Show')),
            genre       TEXT,
            rating      INTEGER CHECK(rating BETWEEN 1 AND 5),
            date_watched TEXT,
            notes       TEXT
        )
    """)
    con.commit()
    con.close()
    print("Database initialised — table 'watched' is ready.")


# ── CREATE ────────────────────────────────────────────────────────────────────

def add_entry(title, type_, genre, rating, date_watched, notes):
    con = get_connection()
    cur = con.cursor()
    cur.execute(
        """
        INSERT INTO watched (title, type, genre, rating, date_watched, notes)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (title, type_, genre, rating, date_watched, notes),
    )
    con.commit()
    new_id = cur.lastrowid
    con.close()
    return new_id


# ── READ ──────────────────────────────────────────────────────────────────────

def get_all_entries(sort_by="date_watched", order="DESC"):
    """Return all entries, optionally sorted."""
    allowed_sorts = {"date_watched", "rating", "title", "type", "genre"}
    allowed_orders = {"ASC", "DESC"}
    if sort_by not in allowed_sorts:
        sort_by = "date_watched"
    if order.upper() not in allowed_orders:
        order = "DESC"
    con = get_connection()
    cur = con.cursor()
    cur.execute(f"SELECT * FROM watched ORDER BY {sort_by} {order.upper()}")
    rows = cur.fetchall()
    con.close()
    return rows


def search_entries(query="", genre_filter="", type_filter="", min_rating=1):
    """
    Filter entries by:
      - title search (partial, case-insensitive)
      - genre
      - type (Movie / TV Show)
      - minimum star rating
    """
    con = get_connection()
    cur = con.cursor()

    sql = "SELECT * FROM watched WHERE 1=1"
    params = []

    if query:
        sql += " AND title LIKE ?"
        params.append(f"%{query}%")
    if genre_filter:
        sql += " AND genre = ?"
        params.append(genre_filter)
    if type_filter:
        sql += " AND type = ?"
        params.append(type_filter)
    if min_rating:
        sql += " AND rating >= ?"
        params.append(min_rating)

    sql += " ORDER BY date_watched DESC"
    cur.execute(sql, params)
    rows = cur.fetchall()
    con.close()
    return rows


def get_entry_by_id(entry_id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM watched WHERE id = ?", (entry_id,))
    row = cur.fetchone()
    con.close()
    return row


def get_distinct_genres():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT DISTINCT genre FROM watched WHERE genre IS NOT NULL ORDER BY genre")
    genres = [row[0] for row in cur.fetchall()]
    con.close()
    return genres


# ── UPDATE ────────────────────────────────────────────────────────────────────

def update_entry(entry_id, title, type_, genre, rating, date_watched, notes):
    con = get_connection()
    cur = con.cursor()
    cur.execute(
        """
        UPDATE watched
        SET title=?, type=?, genre=?, rating=?, date_watched=?, notes=?
        WHERE id=?
        """,
        (title, type_, genre, rating, date_watched, notes, entry_id),
    )
    con.commit()
    affected = cur.rowcount
    con.close()
    return affected  # 1 if updated, 0 if id not found


# ── DELETE ────────────────────────────────────────────────────────────────────

def delete_entry(entry_id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM watched WHERE id = ?", (entry_id,))
    con.commit()
    affected = cur.rowcount
    con.close()
    return affected  # 1 if deleted, 0 if id not found


# ── Run directly to initialise ────────────────────────────────────────────────
if __name__ == "__main__":
    init_db()
