import psycopg2


class DBManager:
    """Класс подключается к БД PostgreSQL."""
    def __init__(self, params):
        self.conn = psycopg2.connect(dbname='hh', **params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        self.cur.execute(f"select company_name, open_vacancies from employers")
        return self.cur.fetchall()

    def get_all_vacancies(self):
        self.cur.execute(f"select employers.company_name, vacancies.vacancy_name, vacancies.salary_from, vacancies.vacancy_url from vacancies "
                         f"join employers using(employer_id)")
        return self.cur.fetchall()

    def get_avg_salary(self):
        self.cur.execute(f"select avg(salary_from) from vacancies")
        return self.cur.fetchall()

    def get_vacancies_with_higher_salary(self):
        self.cur.execute(f"select vacancy_name, salary_from from vacancies "
                         f"group by vacancy_name, salary_from having salary_from > (select avg(salary_from) from vacancies)"
                         f"order by salary_from")
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, word):
        q = """SELECT * FROM vacancies
                        WHERE LOWER(vacancy_name) LIKE %s"""
        self.cur.execute(q, ('%' + word.lower() + '%',))
        return self.cur.fetchall()
