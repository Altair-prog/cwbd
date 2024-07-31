import psycopg2
from typing import List, Tuple


class DBManager:
    """Класс подключается к БД PostgreSQL."""

    def __init__(self, params: dict):
        self.conn = psycopg2.connect(dbname='hh', **params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        self.cur.execute("SELECT company_name, open_vacancies FROM employers")
        return self.cur.fetchall()

    def get_all_vacancies(self) -> List[Tuple[str, str, int, str]]:
        self.cur.execute("""
            SELECT employers.company_name, vacancies.vacancy_name, vacancies.salary_from, vacancies.vacancy_url
            FROM vacancies
            JOIN employers USING(employer_id)
        """)
        return self.cur.fetchall()

    def get_avg_salary(self) -> List[Tuple[float]]:
        self.cur.execute("SELECT AVG(salary_from) FROM vacancies")
        return self.cur.fetchall()

    def get_vacancies_with_higher_salary(self) -> List[Tuple[str, int]]:
        self.cur.execute("""
            SELECT vacancy_name, salary_from
            FROM vacancies
            GROUP BY vacancy_name, salary_from
            HAVING salary_from > (SELECT AVG(salary_from) FROM vacancies)
            ORDER BY salary_from
        """)
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, word: str) -> List[Tuple[int, str, int, str]]:
        self.cur.execute("""
            SELECT * FROM vacancies
            WHERE LOWER(vacancy_name) LIKE %s
        """, ('%' + word.lower() + '%',))
        return self.cur.fetchall()

    def close(self) -> None:
        """Закрытие соединения с базой данных."""
        self.cur.close()
        self.conn.close()
