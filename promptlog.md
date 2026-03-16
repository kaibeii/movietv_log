# Prompt Log — Movie/TV Watch Log

**AI Models Used:** Claude Sonnet 4.6

---

## Prompts & Responses

### 1. Schema Design

**Prompt:**
> "Okay I want to do a movie/TV log. Here are the columns I'm thinking of: id, title, type (movie or TV show), genre, rating from 1 to 5, date watched, notes. Can you help me sketch out the schema and suggest data types for each column?"

**Response:**
Claude laid out the schema as a table with SQLite data types — `INTEGER` for `id` and `rating`, `TEXT` for everything else. It noted that `rating` should have a `CHECK` constraint between 1 and 5, and that `type` should be constrained to `'Movie'` or `'TV Show'`. I confirmed I was happy with it and we moved on.

---

### 2. Database Setup

**Prompt:**
> "Write me a database.py file that connects to a SQLite database and creates the watched table using the schema we designed."

**Response:**
Claude wrote `database.py` with a `get_connection()` helper and an `init_db()` function containing the full `CREATE TABLE IF NOT EXISTS` statement. It used parameterized queries and `row_factory = sqlite3.Row` so rows could be accessed like dictionaries. I ran the file and confirmed the `.db` file was created successfully.

---

### 3. Create (INSERT)

**Prompt:**
> "Add an add_entry() function to database.py that inserts a new row. Use parameterized queries."

**Response:**
Claude added `add_entry()` to `database.py`, taking all the column values as arguments and using `?` placeholders to safely insert them. It returned `cur.lastrowid` so the new entry's ID would be available after insertion. I tested it manually by calling the function from a quick test script and verified the row appeared in the database.

---

### 4. Read (SELECT)

**Prompt:**
> "Add read functions. I want to be able to get all entries with sorting, and also search/filter by title, genre, type, and minimum rating."

**Response:**
Claude added two functions: `get_all_entries()` with `sort_by` and `order` parameters (whitelisted to prevent SQL injection), and `search_entries()` which builds a dynamic `WHERE` clause based on whichever filters are provided. It also added `get_entry_by_id()` and `get_distinct_genres()` as helpers. I tested several filter combinations and the queries returned correct results.

---

### 5. Update & Delete

**Prompt:**
> "Add update_entry() and delete_entry() functions to database.py."

**Response:**
Claude added both functions. `update_entry()` takes all fields plus the entry ID and runs an `UPDATE` statement. `delete_entry()` removes a row by ID. Both return `cur.rowcount` so the caller can tell if the operation actually matched a record. I tested updating a rating and deleting a test entry.

---

### 6. Flask Web Interface

**Prompt:**
> "Build the web interface now using Flask. I want pages for viewing all entries, searching/filtering, adding, editing, and deleting."

**Response:**
Claude created `app.py` with five routes: `/` (list + sort), `/search` (filter), `/add`, `/edit/<id>`, and `/delete/<id>`. It also built five HTML templates using Jinja2 — a shared `base.html` plus `index.html`, `search.html`, `add.html`, and `edit.html`. I ran the app and tested the full CRUD flow and verified via terminal as well.

---

### 7. Refinements

#### External Stylesheet

**Prompt:**
> "Make a separate file called styles.css and remove all the styles from the templates into that file."

**Response:**
Claude extracted all inline `<style>` blocks from every template into a single `static/styles.css` and updated `base.html` to link to it via `url_for('static', filename='styles.css')`.

---

#### Genre Multi-Select

**Prompt:**
> "Make the genre a dropdown instead of a manual text field. They should also be able to select multiple genres."

**Response:**
Claude replaced the text input with a custom pill-based checkbox UI. In `app.py` it switched to `request.form.getlist("genre")` and joined the selections into a comma-separated string before saving. The edit form pre-checks the genres already saved for that entry.

---

#### Custom Font

**Prompt:**
> "I want to change the font of the CineLog logo to be OffBit. The font should also be used as the header font throughout the app."

**Response:**
I uploaded the `OffBit-DotBold.ttf` file. Claude added a `@font-face` declaration in `styles.css` pointing to the font in the `static/` folder, then applied it to `.nav-logo`, `.page-heading`, `.entry-title`, and `.stat-num`.