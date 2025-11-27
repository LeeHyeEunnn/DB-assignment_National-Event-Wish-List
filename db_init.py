import sqlite3

DB_PATH = "event_wishlist.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 공연/행사 정보 테이블
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Event (
        event_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        event_name  TEXT NOT NULL,
        start_date  TEXT,
        end_date    TEXT,
        region      TEXT,
        place       TEXT,
        category    TEXT,
        host        TEXT,
        fee         TEXT,
        homepage    TEXT
    );
    """)

    # 사용자 정보 테이블
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS User (
        user_id     INTEGER PRIMARY KEY AUTOINCREMENT,
        username    TEXT NOT NULL,
        email       TEXT UNIQUE,
        password    TEXT,
        created_at  TEXT DEFAULT (datetime('now', 'localtime'))
    );
    """)

     # 찜 목록 테이블 (User-Event 연결)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Wishlist (
        user_id     INTEGER NOT NULL,
        event_id    INTEGER NOT NULL,
        created_at  TEXT DEFAULT (datetime('now', 'localtime')),
        PRIMARY KEY (user_id, event_id),
        FOREIGN KEY (user_id) REFERENCES User(user_id),
        FOREIGN KEY (event_id) REFERENCES Event(event_id)
    );
    """)

    conn.commit()
    conn.close()
    print("Event 테이블 생성 완료 (DB 파일:", DB_PATH, ")")


if __name__ == "__main__":
    init_db()

