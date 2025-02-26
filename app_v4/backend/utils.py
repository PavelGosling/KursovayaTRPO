from sqlalchemy.orm import Session
from backend import models, schemas

# Функция для поиска издания по названию
def search_edition(db: Session, title: str):
    return db.query(models.Edition).filter(models.Edition.title == title).first()

# Функция для поиска редакции по названию издания
def search_editorial(db: Session, edition_title: str):
    return db.query(models.Editorial).filter(models.Editorial.edition_title == edition_title).first()

# Функция для добавления издания
def add_edition(db: Session, edition_data: schemas.EditionCreate):
    db_edition = models.Edition(**edition_data.dict())
    db.add(db_edition)
    db.commit()
    db.refresh(db_edition)
    return db_edition

# Функция для добавления редакции
def add_editorial(db: Session, editorial_data: schemas.EditorialCreate):
    db_editorial = models.Editorial(**editorial_data.dict())
    db.add(db_editorial)
    db.commit()
    db.refresh(db_editorial)
    return db_editorial

# Функция для удаления издания
def delete_edition(db: Session, title: str):
    db_edition = search_edition(db, title=title)
    if db_edition is None:
        return None
    db.delete(db_edition)
    db.commit()
    return db_edition

# Функция для удаления редакции
def delete_editorial(db: Session, edition_title: str):
    db_editorial = search_editorial(db, edition_title=edition_title)
    if db_editorial is None:
        return None
    db.delete(db_editorial)
    db.commit()
    return db_editorial