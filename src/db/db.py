import sqlite3
from typing import Optional

from .db_connect import get_connection

def save_url(original_url: str, short_code: str, expires_at: str) -> bool:
    """Сохраняет URL в базу данных"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO urls (original_url, short_code, expires_at)
                VALUES (?, ?, ?)
            """, (original_url, short_code, expires_at))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False

def get_url(short_code: str) -> Optional[dict]:
    """Получает URL по короткому коду"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT original_url, clicks, expires_at
            FROM urls 
            WHERE short_code = ? AND (expires_at IS NULL OR expires_at > datetime('now'))
        """, (short_code,))
        result = cursor.fetchone()
        if result:
            return dict(result)
        return None

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

def get_all_urls() -> list:
    """Получает все URL (для отладки)"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM urls")
        return [dict(row) for row in cursor.fetchall()]