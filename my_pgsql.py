import sys
import keyboard
import psycopg2
import traceback
from configparser import ConfigParser


DB_NAME = 'mydb'  # БД PostgreeSQL 12
TABLE_NAME = 'product'  # Наименование таблицы в БД (если не существует, то создаётся новая)


def config(filename='mydb.ini', section='postgresql'):
    """ Читаем и парсим данные для подключения из ini файла.
    Взято тут https://www.postgresqltutorial.com/postgresql-python/connect/ """

    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db


def run_query(query, query_param=()):
    """ Подключение к БД и выполнение запроса """
    try:
        # psycopg2.connect(database="db", user="postgres", password="*", host="127.0.0.1", port="5432")
        params = config()
        with psycopg2.connect(**params) as conn:
            conn.autocommit = True
            cursor = conn.cursor()
            query_result = cursor.execute(query, query_param)
            #conn.commit()
        return query_result
    except Exception:  # noqa # Отлавливаем широкий круг ошибок для вывода в консоль
        print("Exception in user code:")
        print("-" * 60)
        traceback.print_exc(file=sys.stdout)
        print("-" * 60)
        return 'None'


def view_query(query_view):
    """ Подллючение к БД и вывод данных в консоль """
    try:
        params = config()
        with psycopg2.connect(**params) as conn:
            cursor = conn.cursor()
            cursor.execute(query_view)
            query_result = cursor.fetchall()
        if query_result:
            for row in query_result:
                print("| {0:5d} | {1:50s} | {2:20s} |".format(row[0], row[1], row[2]))
            print('-'*85)
        else:
            print('Пусто')
    except Exception:  # noqa # Отлавливаем широкий круг ошибок для вывода в консоль
        print("Exception in user code:")
        print("-" * 60)
        traceback.print_exc(file=sys.stdout)
        print("-" * 60)


if __name__ == '__main__':
    # SELECT datname FROM pg_database; # посмотреть список БД
    # SELECT tablename FROM pg_tables WHERE schemaname='public'; # посмотреть список таблиц в БД

    query = (
        # Удаляем таблицу в БД, если есть(только для PostgreeSQL version >9.1)
        "DROP TABLE IF EXISTS {} CASCADE".format(TABLE_NAME),
        # Создаем таблицу в БД, если нету(только для PostgreeSQL version >9.1)
        "CREATE TABLE IF NOT EXISTS {} "
        "(p_id SERIAL PRIMARY KEY, name VARCHAR(100) NOT NULL, price MONEY NOT NULL DEFAULT 0)".format(TABLE_NAME),
        # Создаем хранимые процедуры
        # Добавить запись
        "CREATE OR REPLACE PROCEDURE product_add(new_name VARCHAR(100), new_price MONEY DEFAULT 0) \
        LANGUAGE 'sql' \
        AS $BODY$ \
            INSERT INTO {} (name, price) VALUES(new_name, new_price); \
        $BODY$;" \
        .format(TABLE_NAME),
        # Изменить запись
        "CREATE OR REPLACE PROCEDURE product_edit(new_p_id INTEGER, new_name VARCHAR(100), new_price MONEY DEFAULT 0) \
        LANGUAGE 'sql' \
        AS $BODY$ \
            UPDATE {} SET name=new_name, price=new_price WHERE p_id=new_p_id; \
        $BODY$;" \
        .format(TABLE_NAME),
        # Удалить запись
        "CREATE OR REPLACE PROCEDURE product_del(new_p_id INTEGER) \
        LANGUAGE 'sql' \
        AS $BODY$ \
            DELETE FROM {} WHERE p_id=new_p_id; \
        $BODY$;" \
        .format(TABLE_NAME)
    )
    for q in query:
        run_query(q)

    # add
    run_query("CALL product_add(%s::VARCHAR(100), %s::MONEY)", ('power cable', 10))
    run_query("CALL product_add(%s::VARCHAR(100), %s::MONEY)", ('mouse', 100))
    run_query("CALL product_add(%s::VARCHAR(100), %s::MONEY)", ('keyboard', 200))
    view_query("SELECT * FROM {};".format(TABLE_NAME))

    # edit
    run_query("CALL product_edit(%s, %s::VARCHAR(100), %s::MONEY)", (2, 'CPU', 1499.99))
    view_query("SELECT * FROM {};".format(TABLE_NAME))

    # del
    run_query("CALL product_del(%s)", (1,))
    view_query("SELECT * FROM {};".format(TABLE_NAME))

    while True:
        print(' Выполнено.\n Для очистки БД от изменений, нажмите клавишу "c"\n Для выхода "q"')
        if keyboard.read_key() == "c":
            # Чистим все что натворили в БД(только для PostgreeSQL version >9.1)
            query = (
                "DROP TABLE IF EXISTS {} CASCADE".format(TABLE_NAME),
                "DROP PROCEDURE IF EXISTS product_add CASCADE",
                "DROP PROCEDURE IF EXISTS product_edit CASCADE",
                "DROP PROCEDURE IF EXISTS product_del CASCADE"
            )
            for q in query:
                run_query(q)
        elif keyboard.is_pressed("q"):
            # Завершаем работу программы
            print('До новых встреч! :)')
            sys.exit()
