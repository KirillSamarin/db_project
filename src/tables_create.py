import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

load_dotenv()


def create_database():
    """Создает базу данных если она не существует"""
    try:
        # Подключаемся к базе данных postgres по умолчанию
        conn = psycopg2.connect(
            port=5432,
            dbname="postgres",
            user=os.getenv("USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("HOST")
        )
        conn.autocommit = True
        cursor = conn.cursor()

        db_name = os.getenv("DB_NAME")
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (db_name,))
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            print(f"База данных {db_name} успешно создана")
        else:
            print(f"База данных {db_name} уже существует")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Ошибка при создании базы данных: {e}")


def create_tables():
    """Создает таблицы companies и vacancies в базе данных"""
    try:
        conn = psycopg2.connect(
            port=5432,
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("HOST")
        )
        cursor = conn.cursor()

        cursor.execute("DROP TABLE IF EXISTS vacancies CASCADE")
        cursor.execute("DROP TABLE IF EXISTS companies CASCADE")

        create_query = sql.SQL("""
        CREATE TABLE companies (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE,
            description TEXT,
            website VARCHAR(255),
            hh_id VARCHAR(50) UNIQUE
        );

        CREATE TABLE vacancies (
            vacancy_id SERIAL PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            description TEXT,
            salary_from INTEGER,
            salary_to INTEGER,
            company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
            hh_vacancy_id VARCHAR(50) UNIQUE
        );
        """)

        cursor.execute(create_query)
        conn.commit()
        print("Таблицы companies и vacancies успешно созданы")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")


if __name__ == "__main__":
    create_database()
    create_tables()


