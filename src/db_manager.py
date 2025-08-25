import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

class DBManager:
    """класс для функций, взаимодействующих с таблицами vacancies и companies"""

    def get_all_vacancies(self):
        """получает все вакансии из таблицы vacanices"""
        conn = psycopg2.connect(
            port=5432,
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("HOST")
        )

        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    v.vacancy_id,
                    v.title,
                    v.description,
                    v.salary_from,
                    v.salary_to,
                    v.hh_vacancy_id,
                    c.name as company_name  -- Добавляем название компании
                FROM vacancies v
                LEFT JOIN companies c ON v.company_id = c.id
                ORDER BY v.vacancy_id
            """)

            vacancies = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]

            result = []
            for vacancy in vacancies:
                result.append(dict(zip(column_names, vacancy)))

            vacancies_return = []

            for vacancy in result:
                vacancies_return.append(f"""{vacancy['company_name']} {vacancy['title']} {vacancy['salary_from']} {vacancy['salary_to']} https://hh.ru/vacancy/{vacancy['hh_vacancy_id']}""")

            return vacancies_return

    def get_companies_and_vacancies_count(self):
        """получает компании и количество их вакансий"""
        conn = psycopg2.connect(
            port=5432,
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("HOST")
            )

        with conn.cursor() as cursor:
                # Используем LEFT JOIN и GROUP BY для подсчета вакансий
            cursor.execute("""
                SELECT 
                    c.name as company_name,
                    COUNT(v.vacancy_id) as vacancies_count
                    FROM companies c
                    LEFT JOIN vacancies v ON c.id = v.company_id
                    GROUP BY c.id, c.name
                    ORDER BY vacancies_count DESC
                """)

            companies = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]

            result = []
            for company in companies:
                result.append(dict(zip(column_names, company)))

            return result

    def get_avg_salary(self):
        """считает минимальную среднюю зарплату"""
        conn = psycopg2.connect(
            port=5432,
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("HOST")
        )

        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COALESCE(ROUND(AVG(salary_from)), 0) 
                FROM vacancies 
                WHERE salary_from IS NOT NULL
            """)

            avg_salary = cursor.fetchone()[0]
            return int(avg_salary)

    def get_vacancies_with_higher_salary(self):
        """возвращает вакансии, чья зарплата выше чем средняя(get_avg_salary())"""
        conn = psycopg2.connect(
            port=5432,
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("HOST")
        )

        with conn.cursor() as cursor:
            avg_salary = DBManager.get_avg_salary(self)
            cursor.execute(f"""
                SELECT v.*, c.name as company_name 
                FROM vacancies v
                LEFT JOIN companies c ON v.company_id = c.id
                WHERE v.salary_from > {avg_salary}
                ORDER BY v.salary_from DESC
            """)

            vacancies = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]

            result = []
            for vacancy in vacancies:
                result.append(dict(zip(column_names, vacancy)))

            return result

    def get_vacancies_with_keyword(self, keyword: str):
        """возвращает все вакансии, содержащие определенное слово"""
        conn = psycopg2.connect(
            port=5432,
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("HOST")
        )

        with conn.cursor() as cursor:
            cursor.execute(f"""SELECT v.*, c.name as company_name 
                FROM vacancies v
                LEFT JOIN companies c ON v.company_id = c.id
                WHERE title LIKE '%{keyword}%'""")

            vacancies = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]

            result = []
            for vacancy in vacancies:
                result.append(dict(zip(column_names, vacancy)))

            return result

if __name__ == "__main__":
    pass



