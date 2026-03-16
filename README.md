# CineLog — Movie & TV Watch Log

A Flask web app backed by SQLite for tracking movies and TV shows you've watched.

## What It Tracks

I built this to keep a personal record of everything I've watched — movies and TV shows — with a star rating, genre, date, and personal notes.

---

## Database Schema

**Table: `watched`**

| Column        | Type    | Description                              |
|---------------|---------|------------------------------------------|
| `id`          | INTEGER | Primary key, auto-incremented            |
| `title`       | TEXT    | Title of the movie or TV show (required) |
| `type`        | TEXT    | `"Movie"` or `"TV Show"`                 |
| `genre`       | TEXT    | Genre (e.g. Sci-Fi, Drama, Comedy)       |
| `rating`      | INTEGER | Star rating from 1 to 5                  |
| `date_watched`| TEXT    | Date watched (YYYY-MM-DD)                |
| `notes`       | TEXT    | Personal notes or thoughts               |

---

## Setup & Running

**Requirements:** Python 3.7+

1. Install Flask:
   ```bash
   pip install flask
   ```

2. Run the app (this also initialises the database on first run):
   ```bash
   python app.py
   ```

3. Open your browser to: [http://127.0.0.1:5000](http://127.0.0.1:5000)

No other dependencies — `sqlite3` is part of Python's standard library.

---

## CRUD Operations

### Create — Add an Entry
Click **"+ Add"** in the top navigation bar. Fill in the title, type (Movie or TV Show), genre, star rating, date watched, and optional notes, then click **Save Entry**.

### Read — View & Sort All Entries
The home page (`/`) displays all logged entries as cards. Use the **Sort by** and **↓ Desc / ↑ Asc** dropdowns to reorder by date watched, rating, title, type, or genre.

### Read (filtered) — Search
Click **Search** in the nav. Filter by:
- Title keyword (partial match)
- Type (Movie / TV Show)
- Genre (populated from your existing entries)
- Minimum star rating

### Update — Edit an Entry
Click the **Edit** button on any card. Modify any fields and click **Update Entry**.

### Delete — Remove an Entry
Click the **Delete** button on any card. A confirmation dialog appears before the entry is permanently removed.

---

## File Structure

```
movie_log/
├── app.py          # Flask routes
├── database.py     # SQLite helper functions (all CRUD logic)
├── movie_log.db    # Created automatically on first run
└── templates/
    ├── base.html   # Shared layout & styles
    ├── index.html  # Home — list & sort all entries
    ├── add.html    # Add new entry form
    ├── edit.html   # Edit existing entry form
    └── search.html # Filter/search page
```
