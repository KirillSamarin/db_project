import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

load_dotenv()

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
cursor.close()
conn.close()


