from db_manager import DBManager

db = DBManager()


def user_interface():
    print("Вас приветствует программа для работы с вакансиями и компаниями,")
    print("сохраненных в вашей базе данных.")

    while True:
        print("\nВыберите интересующую вас функцию:")
        print("1. Получить список всех вакансий")
        print("2. Получить список всех компаний и количество их вакансий")
        print("3. Получить среднюю зарплату по всем вакансиям")
        print("4. Получить все вакансии, зарплата которых выше средней")
        print("5. Получить все вакансии, содержащие определенное слово")
        print("0. Выйти из программы")

        try:
            user_input = int(input("Ваш выбор: "))

            if user_input == 0:
                print("До свидания!")
                break

            elif user_input == 1:
                print("СПИСОК ВСЕХ ВАКАНСИЙ:")
                vacancies = db.get_all_vacancies()
                if vacancies:
                    for i, vacancy in enumerate(vacancies, 1):
                        print(f"{i}. {vacancy}")
                else:
                    print("В базе данных нет вакансий.")

            elif user_input == 2:
                print("КОМПАНИИ И КОЛИЧЕСТВО ВАКАНСИЙ:")
                companies = db.get_companies_and_vacancies_count()
                if companies:
                    for company in companies:
                        print(f"{company['company_name']}: {company['vacancies_count']} вакансий")
                else:
                    print("В базе данных нет компаний.")

            elif user_input == 3:
                print("СРЕДНЯЯ ЗАРПЛАТА ПО ВАКАНСИЯМ:")
                avg_salary = db.get_avg_salary()
                print(f"Средняя зарплата: {avg_salary:,} руб.".replace(',', ' '))

            elif user_input == 4:
                print("ВАКАНСИИ С ЗАРПЛАТОЙ ВЫШЕ СРЕДНЕЙ:")
                vacancies = db.get_vacancies_with_higher_salary()
                if vacancies:
                    for i, vacancy in enumerate(vacancies, 1):
                        salary_info = ""
                        if vacancy['salary_from']:
                            salary_info += f"от {vacancy['salary_from']:,} руб. "
                        if vacancy['salary_to']:
                            salary_info += f"до {vacancy['salary_to']:,} руб."
                        print(f"{i}. {vacancy['company_name']} - {vacancy['title']}")
                        print(f"   Зарплата: {salary_info if salary_info else 'не указана'}")
                        print(f"   Ссылка: https://hh.ru/vacancy/{vacancy['hh_vacancy_id']}")
                        print()
                else:
                    print("Вакансий с зарплатой выше средней не найдено.")

            elif user_input == 5:
                print("ПОИСК ВАКАНСИЙ ПО КЛЮЧЕВОМУ СЛОВУ:")
                keyword = input("Введите ключевое слово для поиска: ").strip()
                if keyword:
                    vacancies = db.get_vacancies_with_keyword(keyword)
                    if vacancies:
                        print(f"\nНайдено {len(vacancies)} вакансий по запросу '{keyword}':")
                        print("-" * 60)
                        for i, vacancy in enumerate(vacancies, 1):
                            salary_info = ""
                            if vacancy['salary_from']:
                                salary_info += f"от {vacancy['salary_from']:,} руб. "
                            if vacancy['salary_to']:
                                salary_info += f"до {vacancy['salary_to']:,} руб."
                            print(f"{i}. {vacancy['company_name']} - {vacancy['title']}")
                            print(f"   Зарплата: {salary_info if salary_info else 'не указана'}")
                            print(f"   Ссылка: https://hh.ru/vacancy/{vacancy['hh_vacancy_id']}")
                            print()
                    else:
                        print(f"Вакансий по запросу '{keyword}' не найдено.")
                else:
                    print("Вы не ввели ключевое слово для поиска.")

            else:
                print("Неверный выбор. Пожалуйста, выберите число от 0 до 5.")

        except ValueError:
            print("Пожалуйста, введите число!")
        except Exception as e:
            print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    user_interface()