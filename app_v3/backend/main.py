# backend/main.py
from fastapi import FastAPI, Depends, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from backend import models, schemas, utils
from backend.database import engine, get_db
from typing import Annotated
from urllib.parse import urlencode
import os
from pydantic import ValidationError  # Импортируем ValidationError

# Создание таблиц в БД при запуске
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Подключаем шаблонизатор Jinja2 для работы с html
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "frontend"))

# Настройка статических файлов
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "..", "frontend")), name="static")

# Роут главной страницы
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Роут страницы добавления изданий
@app.get("/add_edition", response_class=HTMLResponse)
async def add_edition_form(request: Request, message: str = None):
    return templates.TemplateResponse("add_edition.html", {"request": request, "message": message})

# Роут страницы добавления редакций
@app.get("/add_editorial", response_class=HTMLResponse)
async def add_editorial_form(request: Request, message: str = None):
    return templates.TemplateResponse("add_editorial.html", {"request": request, "message": message})

# Роут страницы удаления изданий
@app.get("/delete_edition", response_class=HTMLResponse)
async def delete_edition_form(request: Request, message: str = None):
    return templates.TemplateResponse("delete_edition.html", {"request": request, "message": message})

# Роут страницы удаления редакций
@app.get("/delete_editorial", response_class=HTMLResponse)
async def delete_editorial_form(request: Request, message: str = None):
    return templates.TemplateResponse("delete_editorial.html", {"request": request, "message": message})

# Роут страницы поиска данных в БД
@app.get("/search", response_class=HTMLResponse)
async def search_form(request: Request, message: str = None):
    return templates.TemplateResponse("search.html", {"request": request, "message": message})

# --- API Endpoints ---

# Получение всех изданий и редакций
@app.get("/editions")
async def get_editions(db: Session = Depends(get_db)) -> list[dict]:
    # Получаем все издания и редакции из базы данных
    editions = db.query(models.Edition).all()
    editorials = db.query(models.Editorial).all()

    # Собираем все данные в один список
    editions_data = []
    
    # Добавляем издания
    for edition in editions:
        editorial = next((e for e in editorials if e.edition_title == edition.title), None)
        editions_data.append({
            "title": edition.title,
            "type": edition.type,
            "publisher": edition.publisher,
            "year": edition.year,
            "address": editorial.address if editorial else "Нет данных",
            "editor_in_chief": editorial.editor_in_chief if editorial else "Нет данных"
        })
    
    # Добавляем редакции, которые не связаны с изданиями
    for editorial in editorials:
        if not any(edition['title'] == editorial.edition_title for edition in editions_data):
            editions_data.append({
                "title": editorial.edition_title,
                "type": "Нет данных",
                "publisher": "Нет данных",
                "year": "Нет данных",
                "address": editorial.address,
                "editor_in_chief": editorial.editor_in_chief
            })
    
    return editions_data

# Добавление издания
@app.post("/add_edition", response_class=RedirectResponse)
async def create_edition(
    request: Request,
    title: Annotated[str, Form()],
    type: Annotated[str, Form()],
    publisher: Annotated[str, Form()],
    year: Annotated[int, Form()],
    db: Session = Depends(get_db)
):
    try:
        # Валидация данных через Pydantic
        edition_data = schemas.EditionCreate(title=title, type=type, publisher=publisher, year=year)
    except ValidationError as e:
        # Обработка ошибки валидации
        error_message = e.errors()[0]["msg"]  # Получаем первое сообщение об ошибке
        query_params = urlencode({"message": error_message})
        return RedirectResponse(url=f"/add_edition?{query_params}", status_code=303)
    except ValueError as e:
        # Обработка ошибки валидации года
        query_params = urlencode({"message": str(e)})
        return RedirectResponse(url=f"/add_edition?{query_params}", status_code=303)
    except Exception as e:
        # Обработка всех остальных исключений
        query_params = urlencode({"message": f"Произошла ошибка: {str(e)}"})
        return RedirectResponse(url=f"/add_edition?{query_params}", status_code=303)

    # Создание записи в базе данных
    db_edition = models.Edition(**edition_data.dict())
    db.add(db_edition)
    db.commit()
    db.refresh(db_edition)
    
    query_params = urlencode({"message": "Издание успешно добавлено!"})
    return RedirectResponse(url=f"/add_edition?{query_params}", status_code=303)

# Добавление редакции
@app.post("/add_editorial", response_class=RedirectResponse)
async def create_editorial(
    request: Request,
    edition_title: Annotated[str, Form()],
    address: Annotated[str, Form()],
    editor_in_chief: Annotated[str, Form()],
    db: Session = Depends(get_db)
):
    try:
        # Валидация данных через Pydantic
        editorial_data = schemas.EditorialCreate(edition_title=edition_title, address=address, editor_in_chief=editor_in_chief)
    except ValidationError as e:
        # Обработка ошибки валидации
        error_message = e.errors()[0]["msg"]  # Получаем первое сообщение об ошибке
        query_params = urlencode({"message": error_message})
        return RedirectResponse(url=f"/add_editorial?{query_params}", status_code=303)
    except Exception as e:
        # Обработка всех остальных исключений
        query_params = urlencode({"message": f"Произошла ошибка: {str(e)}"})
        return RedirectResponse(url=f"/add_editorial?{query_params}", status_code=303)

    # Создание записи в базе данных
    db_editorial = models.Editorial(**editorial_data.dict())
    db.add(db_editorial)
    db.commit()
    db.refresh(db_editorial)
    
    query_params = urlencode({"message": "Редакция успешно добавлена!"})
    return RedirectResponse(url=f"/add_editorial?{query_params}", status_code=303)

# Удаление издания
@app.post("/delete_edition", response_class=RedirectResponse)
async def delete_edition(
    request: Request,
    title: Annotated[str, Form()],
    db: Session = Depends(get_db)
):
    try:
        db_edition = utils.search_edition(db, title=title)
        if db_edition is None:
            query_params = urlencode({"message": "Издание не найдено!"})
            return RedirectResponse(url=f"/delete_edition?{query_params}", status_code=303)
        db.delete(db_edition)
        db.commit()
        query_params = urlencode({"message": "Издание успешно удалено!"})
        return RedirectResponse(url=f"/delete_edition?{query_params}", status_code=303)
    except Exception as e:
        # Обработка всех остальных исключений
        query_params = urlencode({"message": f"Произошла ошибка: {str(e)}"})
        return RedirectResponse(url=f"/delete_edition?{query_params}", status_code=303)

# Удаление редакции
@app.post("/delete_editorial", response_class=RedirectResponse)
async def delete_editorial(
    request: Request,
    edition_title: Annotated[str, Form()],
    db: Session = Depends(get_db)
):
    try:
        db_editorial = utils.search_editorial(db, edition_title=edition_title)
        if db_editorial is None:
            query_params = urlencode({"message": "Редакция не найдена!"})
            return RedirectResponse(url=f"/delete_editorial?{query_params}", status_code=303)
        db.delete(db_editorial)
        db.commit()
        query_params = urlencode({"message": "Редакция успешно удалена!"})
        return RedirectResponse(url=f"/delete_editorial?{query_params}", status_code=303)
    except Exception as e:
        # Обработка всех остальных исключений
        query_params = urlencode({"message": f"Произошла ошибка: {str(e)}"})
        return RedirectResponse(url=f"/delete_editorial?{query_params}", status_code=303)