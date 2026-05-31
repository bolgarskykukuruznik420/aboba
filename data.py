import sqlite3

conn = sqlite3.connect("filters.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS filters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    category TEXT,
    min_price INTEGER,
    max_price INTEGER,
    condition INTEGER NOT NULL,
    search_query TEXT, 
    active INTEGER DEFAULT 0
)
""")

conn.commit()


def add_filter(
    user_id,
    category,
    search_query,
    condition,
    min_price,
    max_price
):
    cursor.execute(
        """
        INSERT INTO filters (
            user_id,
            category,
            search_query,
            condition,
            min_price,
            max_price
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            category,
            search_query,
            condition,
            min_price,
            max_price
        )
    )

    conn.commit()


def get_filters(user_id):
    cursor.execute(
        "SELECT * FROM filters WHERE user_id = ?",
        (user_id,)
    )

    return cursor.fetchall()

cursor.execute("""
CREATE TABLE IF NOT EXISTS seen_items (
    item_url TEXT PRIMARY KEY
)
""")

conn.commit()


def is_seen(url):

    cursor.execute(
        "SELECT item_url FROM seen_items WHERE item_url = ?",
        (url,)
    )

    return cursor.fetchone()


def add_seen(url):

    cursor.execute(
        "INSERT OR IGNORE INTO seen_items VALUES (?)",
        (url,)
    )

    conn.commit()


def get_all_filters():

    cursor.execute(
        "SELECT * FROM filters"
    )

    return cursor.fetchall()

def delete_filter(filter_id, user_id):

    cursor.execute(
        """
        DELETE FROM filters
        WHERE id = ? AND user_id = ?
        """,
        (filter_id, user_id)
    )

    conn.commit()

def set_active_filter(filter_id, user_id):

    cursor.execute(
        """
        UPDATE filters
        SET active = 0
        WHERE user_id = ?
        """,
        (user_id,)
    )

    cursor.execute(
        """
        UPDATE filters
        SET active = 1
        WHERE id = ? AND user_id = ?
        """,
        (filter_id, user_id)
    )

    conn.commit()

def get_active_filters():

    cursor.execute(
        """
        SELECT *
        FROM filters
        WHERE active = 1
        """
    )

    return cursor.fetchall()

