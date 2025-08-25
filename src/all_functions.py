from db_manager import DBManager
import hh_api

db = DBManager()

hh_api.fill_table_companies()
hh_api.fill_table_vacancies(company_ids=3529)

db.get_companies_and_vacancies_count()
db.get_all_vacancies()
db.get_avg_salary()
db.get_vacancies_with_higher_salary()
db.get_vacancies_with_keyword("")