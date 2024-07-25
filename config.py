from configparser import ConfigParser


def config(filename="database.ini", section="postgresql"):
    # Создаем парсер
    parser = ConfigParser()

    # Читаем файл конфигурации
    parser.read(filename)

    # Инициализируем пустой словарь для параметров базы данных
    db = {}

    # Проверяем, есть ли указанный раздел в файле конфигурации
    if parser.has_section(section):
        # Получаем все параметры из указанного раздела
        params = parser.items(section)
        # Добавляем каждый параметр в словарь
        for param in params:
            db[param[0]] = param[1]
    else:
        # Если раздел не найден, генерируем исключение с сообщением об ошибке
        raise Exception(
            'Раздел {0} не найден в файле {1}.'.format(section, filename))

    # Возвращаем словарь с параметрами базы данных
    return db
