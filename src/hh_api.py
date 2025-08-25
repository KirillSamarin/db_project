import requests
import psycopg2
from psycopg2 import sql
import re
from dotenv import load_dotenv
import os

load_dotenv()


conn = psycopg2.connect(
    port=5432,
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("HOST")
)
cursor = conn.cursor()

IDS = {"EMPLOYER_ID_SBER": "3529",
"EMPLOYER_ID_X5": "4716984",
"EMPLOYER_ID_TBANK": "78638",
"EMPLOYER_ID_SOCISM": "3468783",
"EMPLOYER_ID_MAGNIT": "49357",
"EMPLOYER_ID_F5": "1308904",
"EMPLOYER_ID_MTS": "3776",
"EMPLOYER_ID_MEGAPHON": "3127",
"EMPLOYER_ID_IRBIS": "2961124",
"EMPLOYER_ID_KEYSYSTEMS": "120583"}


def fill_table_companies():
    """Заполняет таблицу компаний и возвращаем словарь с их ID"""
    company_ids = {}

    for hh_id in IDS.values():
        response = requests.get(f"https://api.hh.ru/employers/{hh_id}")
        data = response.json()

        clean = re.compile("<.*?>")
        description = re.sub(clean, "", data.get("description", ""))

        company_data = {
            "name": data.get("name"),
            "description": description,
            "website": data.get("site_url"),
            "hh_id": hh_id
        }

        insert_query = sql.SQL("""
            INSERT INTO companies (name, description, website, hh_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """)

        cursor.execute(insert_query, (
            company_data["name"],
            company_data["description"],
            company_data["website"],
            company_data["hh_id"]
        ))

        db_id = cursor.fetchone()[0]
        company_ids[hh_id] = db_id

        conn.commit()

    return company_ids


def fill_table_vacancies(company_ids):
    """Заполняет таблицу вакансий с привязкой к компаниям"""

    for hh_id, db_id in company_ids.items():
        response = requests.get(f"https://api.hh.ru/vacancies", params={"employer_id": hh_id, "per_page": 10})
        data = response.json()

        for vacancy in data["items"]:
            salary = vacancy.get("salary")

            # Обрабатываем зарплату
            salary_from = None
            salary_to = None

            if salary:
                salary_from = salary.get("from")
                salary_to = salary.get("to")

            # Очищаем описание от HTML тегов
            clean = re.compile("<.*?>")
            description = re.sub(clean, "", vacancy.get("description", ""))

            insert_query = sql.SQL("""
                INSERT INTO vacancies (title, description, salary_from, salary_to, company_id, hh_vacancy_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """)

            cursor.execute(insert_query, (
                vacancy.get("name"),
                description,
                salary_from or 0,
                salary_to or 0,
                db_id,
                vacancy.get("id")
            ))

        conn.commit()


def main():
    """Основная функция для заполнения базы данных"""
    company_ids = fill_table_companies()
    fill_table_vacancies(company_ids)
    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
