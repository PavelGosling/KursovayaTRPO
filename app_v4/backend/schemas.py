from pydantic import BaseModel, validator
from typing import Optional

# Схема для создания и валидации сущности "Изданий"
class EditionCreate(BaseModel):
    title: str  # Название издания
    type: str  # Вид издания
    publisher: str  # Издающая организация
    year: int  # Год выпуска

    # Валидация года выпуска
    @validator("year")
    def validate_year(cls, value):
        if not 1900 <= value <= 2099:
            raise ValueError("Год выпуска должен быть в диапазоне от 1900 до 2099")
        return value

# Схема для создания и валидации сущности "Редакций"
class EditorialCreate(BaseModel):
    edition_title: str  # Название издания
    address: str  # Адрес организации
    editor_in_chief: str  # Фамилия главного редактора

# Схема для выдачи сущности "Изданий"
class Edition(EditionCreate):
    id: int  # Уникальный идентификатор

    class Config:
        orm_mode = True  # Включение режима ORM для работы с SQLAlchemy

# Схема для выдачи сущности "Редакций"
class Editorial(EditorialCreate):
    id: int  # Уникальный идентификатор

    class Config:
        orm_mode = True  # Включение режима ORM для работы с SQLAlchemy