import sqlite3
from typing import Optional

from db.db_con import get_connection
from src.app.logs.logger import logger_calls

@logger_calls
def save_url(original_url: str, short_code: str) -> bool:
    """Сохраняет URL в базу данных"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO urls (original_url, short_code)
                VALUES (?, ?)
            """, (original_url, short_code))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False

@logger_calls
def get_url(short_code: str) -> Optional[dict]:
    """Получает URL по короткому коду"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT original_url, clicks, short_code, created_at
            FROM urls 
            WHERE short_code = ?
        """, (short_code,))
        result = cursor.fetchone()
        if result:
            return dict(result)
        return None

@logger_calls
def increment_clicks(short_code: str):
    """Увеличивает счетчик кликов"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE urls 
            SET clicks = clicks + 1 
            WHERE short_code = ?
        """, (short_code,))
        conn.commit()

@logger_calls
def get_all_urls() -> list:
    """Получает все URL (для отладки)"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM urls ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]