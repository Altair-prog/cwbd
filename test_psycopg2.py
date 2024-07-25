# test_psycopg2.py
try:
    import psycopg2
    print("psycopg2 успешно импортирован!")
except ModuleNotFoundError:
    print("Модуль psycopg2 не найден.")
