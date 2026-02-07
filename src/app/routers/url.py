from fastapi import APIRouter, HTTPException, status, Body
from fastapi.responses import RedirectResponse
from datetime import datetime
from typing import Optional

from src.app.logs.logger import log_endpoint
from db.db_func import save_url, get_url, increment_clicks, get_all_urls
from app.utils.utils import generate_short_code, is_valid_url

router = APIRouter(prefix="", tags=["urls"])

@router.post("/shorten", status_code=status.HTTP_201_CREATED)
@log_endpoint
async def shorten_url(
    url: str = Body(..., description="Оригинальный URL"),
    custom_code: Optional[str] = Body(None, description="Пользовательский код (опционально)")
):
    """
    Создает короткую версию URL
    
    Пример тела запроса:
    {
        "url": "https://example.com",
        "custom_code": "mycode123"
    }
    """
    valid = is_valid_url(url)
    if not valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Некорректный URL. Должен начинаться с http:// или https://"
        )
    
    if custom_code:
        short_code = custom_code
        if not short_code.isalnum():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Код может содержать только буквы и цифры"
            )
    else:
        short_code = generate_short_code()
    
    created_at = datetime.now().isoformat()
    
    result = save_url(url, short_code)

    if not result:
        if custom_code:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Код '{short_code}' уже используется"
            )
        short_code = generate_short_code()
        new_result = save_url(url, short_code)
        if not new_result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Не удалось сохранить URL. Попробуйте еще раз."
            )
    
    return {
        "short_code": short_code,
        "short_url": f"http://localhost:8000/{short_code}",
        "original_url": url,
        "created_at": created_at
    }

@router.get("/{short_code}")
@log_endpoint
async def redirect_to_url(short_code: str):
    """
    Перенаправляет на оригинальный URL по короткому коду
    """
    url_data = get_url(short_code)
    
    if not url_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ссылка не найдена"
        )
    
    increment_clicks(short_code)
    
    return RedirectResponse(url=url_data["original_url"], status_code=status.HTTP_302_FOUND)

@router.get("/urls/all", tags=["debug"])
@log_endpoint
async def get_all_urls_endpoint():
    """Получить все сокращенные URL (для отладки)"""
    result = get_all_urls()
    return result

@router.get("/urls/{short_code}/info")
@log_endpoint
async def get_url_info(short_code: str):
    """Получить информацию о сокращенной ссылке"""
    url_data = get_url(short_code)
    
    if not url_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ссылка не найдена"
        )
    
    return {
        "short_code": url_data["short_code"],
        "original_url": url_data["original_url"],
        "clicks": url_data["clicks"],
        "created_at": url_data["created_at"],
        "short_url": f"http://localhost:8000/{short_code}"
    }