# backend/utils.py
from sqlalchemy.orm import Session
from backend import models, schemas


# Функция для поиска издания по названию
def search_edition(db: Session, title: str):
    return db.query(models.Edition).filter(
        models.Edition.title == title
    ).first()

# Функция для поиска редакции по названию издания
def search_editorial(db: Session, edition_title: str):
    return db.query(models.Editorial).filter(
        models.Editorial.edition_title == edition_title
    ).first()