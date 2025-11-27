from pathlib import Path
import sqlite3

import pandas as pd

DB_PATH = Path("event_wishlist.db")
CSV_PATH = Path("data") / "전국공연행사정보표준데이터.csv"


def preview_csv():
    """CSV가 제대로 읽히는지 확인용"""
    print("CSV 경로:", CSV_PATH)
    if not CSV_PATH.exists():
        print("CSV 파일을 찾을 수 없습니다.")
        return

    df = pd.read_csv(CSV_PATH, encoding="cp949")
    print("CSV 로드 성공")
    print("행 개수:", len(df))
    print("컬럼 목록:", list(df.columns))
    print()
    print("====== 첫 3개 행 ======")
    print(df.head(3))


def load_events_to_db():
    """CSV를 읽어서 Event 테이블에 데이터 적재"""
    if not CSV_PATH.exists():
        print("CSV 파일을 찾을 수 없습니다:", CSV_PATH)
        return

    # CSV 읽기
    df = pd.read_csv(CSV_PATH, encoding="cp949")
    df = df.fillna("")  # NaN → 빈 문자열

    # '홈페'라는 글자를 포함하는 컬럼을 홈페이지 컬럼으로 사용
    homepage_col = None
    for col in df.columns:
        if "홈페" in col:
            homepage_col = col
            break

    # DB 연결
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 개발 편의: 기존 Event 데이터 삭제 후 새로 채우기
    cursor.execute("DELETE FROM Event;")

    inserted = 0

    for _, row in df.iterrows():
        name = str(row["행사명"]).strip()
        if not name:
            continue  # 행사명이 없으면 스킵

        # 주소에서 시/도만 region으로 추출
        address = row["소재지도로명주소"]
        region = ""
        if isinstance(address, str) and address.strip():
            region = address.split()[0]  # 예: '서울특별시', '인천광역시'

        event_name = name
        start_date = str(row["행사시작일자"]).strip()
        end_date = str(row["행사종료일자"]).strip()
        place = row["장소"].strip() if isinstance(row["장소"], str) else ""

        # 주최/주관 중 하나 선택
        if isinstance(row["주최기관명"], str) and row["주최기관명"].strip():
            host = row["주최기관명"].strip()
        else:
            host = str(row["주관기관명"]).strip()

        fee = str(row["요금정보"]).strip()

        if homepage_col:
            homepage = str(row[homepage_col]).strip()
        else:
            homepage = ""

        cursor.execute(
            """
            INSERT INTO Event (
                event_name, start_date, end_date,
                region, place, category, host, fee, homepage
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event_name,
                start_date,
                end_date,
                region,
                place,
                "",       # category는 나중에 필요하면 채우기
                host,
                fee,
                homepage,
            ),
        )
        inserted += 1

    conn.commit()
    conn.close()

    print(f"Event 테이블에 데이터 적재 완료! 총 {inserted}건 삽입됨.")


if __name__ == "__main__":
    # 필요할 때만 주석 풀어서 사용
    # preview_csv()
    load_events_to_db()
