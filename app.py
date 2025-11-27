from flask import Flask, render_template
import sqlite3
from pathlib import Path

app = Flask(__name__)

DB_PATH = Path("event_wishlist.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 컬럼 이름으로 접근 가능하게
    return conn


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/events")
def event_list():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT event_id, event_name, start_date, end_date, region, place
        FROM Event
        ORDER BY start_date
        LIMIT 50;
    """)
    events = cursor.fetchall()
    conn.close()

    return render_template("events.html", events=events)


if __name__ == "__main__":
    app.run(debug=True)
