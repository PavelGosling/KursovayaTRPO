# backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение URL базы данных из переменных окружения
DATABASE_URL = os.getenv("DATABASE_URL")

# Создаем движок SQLAlchemy для подключения к базе данных.
# Параметр echo=True включает логирование SQL-запросов (удобно для отладки)
engine = create_engine(DATABASE_URL, echo=True)

# Создаем класс для создания сессий (соединений) с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем базовый класс для моделей SQLAlchemy
Base = declarative_base()

# Функция для получения сессии (используется в зависимостях FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()