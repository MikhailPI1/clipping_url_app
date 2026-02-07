import random
import string
from datetime import datetime, timedelta


def generate_short_code(length: int = 6) -> str:
    """
    Генерирует случайный код для короткой ссылки.
    Использует буквы (A-Z, a-z) и цифры (0-9).
    """
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def is_valid_url(url: str) -> bool:
    """
    Проверяет, что URL начинается с http:// или https://
    """
    if not url:
        return False
    return url.startswith(('http://', 'https://'))

def get_expiration_date(days: int = 30) -> str:
    """
    Возвращает дату истечения срока действия.
    По умолчанию - через 30 дней.
    """
    expiration = datetime.now() + timedelta(days=days)
    return expiration.isoformat()