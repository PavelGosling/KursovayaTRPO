# backend/models.py
from sqlalchemy import Column, Integer, String
from backend.database import Base

# Модель для сущности "Изданий"
class Edition(Base):
    __tablename__ = "editions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)  # Название издания
    type = Column(String)  # Вид издания
    publisher = Column(String)  # Издающая организация
    year = Column(Integer)  # Год выпуска

# Модель для сущности "Редакций"
class Editorial(Base):
    __tablename__ = "editorials"

    id = Column(Integer, primary_key=True, index=True)
    edition_title = Column(String, index=True)  # Название издания
    address = Column(String)  # Адрес организации
    editor_in_chief = Column(String)  # Фамилия главного редактора