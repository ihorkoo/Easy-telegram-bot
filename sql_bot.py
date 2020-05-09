import sqlite3
import configparser
import datetime

config = configparser.ConfigParser()
config.read('config.ini')

PATH = config['DB']['Path']


def create_connection(PATH):
    """Конект до бази даних
    :PATH: шлях до бази даних
    return: обєкт conn
    """
    conn  = None

    try:
        conn = sqlite3.connect(PATH)
        return conn
    except Exception as e:
        print(e)
        return conn

def connector(funck):
    def wrapper(*args, **kvargs):
        conn = create_connection(PATH)
        result = None
        if conn == None:
            return result
        else:
            try:
                result = funck(conn, *args, **kvargs)
                return result
            except Exception as e:
                print(e)
            else:
                conn.commit()
            finally:
                conn.close()
            return result
    return wrapper

@connector
def create_table(conn, sql_text):
    """Функція для створення таблиць в базі даних"""
    try:
        c = conn.cursor()        #cursor  - обєкт, для виконання запитів sql
        c.execute(sql_text)      #execute - виконує запити
        return True
    except Exception as e:
        print(e)
        return False

create_table_product = """CREATE TABLE product (Product text PRIMARY KEY,
                          Unit text NOT NULL)
                          """

create_table_sales = """CREATE TABLE sales(
                        Period date NOT NULL,
                        Product text,
                        Qty real NOT NULL,
                        FOREIGN KEY (Product) REFERENCES product (Product))
                        """

@connector
def insert_product(conn, product, unit):
    """Вставляємо дані в таблицю product"""

    sql_text = """INSERT INTO product(Product, Unit) VALUES (?, ?)"""

    c = conn.cursor()
    c.execute(sql_text, (product, unit))

    return True


@connector
def insert_sales(conn, product, qty):
    """Вставляємо дані в таблицю sales"""

    period = datetime.datetime.now()    #datetime.now().isoformat(timespec='minutes')

    sql_text = """INSERT INTO sales (Period, Product, Qty) VALUES (?, ?, ?)"""

    c = conn.cursor()
    c.execute(sql_text, (period, product, qty))

    return True

@connector
def check_product(conn, product):
    """Перевіряємо, чи товар наявний в базі даних"""

    sql_text = """SELECT Count(Product)
                FROM product
                WHERE  Product = (?)
                """
    #[(1,), (), (), ()]
    #[(0,)]
    c = conn.cursor()
    c.execute(sql_text, (product,))

    result = True if c.fetchall()[0][0] == 1 else False

    """if c.fetchall()[0][0] == 1:
        return True
    else:
        return False"""

    return result




#Допоміжні функції

@connector
def select_product(conn):
    sql_text = "SELECT * FROM product"
    c = conn.cursor()
    c.execute(sql_text)
    print(c.fetchall())
    for i in c.fetchall():
        print(i)

@connector
def select_sales(conn):
    sql_text = "SELECT * FROM sales"
    c = conn.cursor()
    c.execute(sql_text)
    print(c.fetchall())
    for i in c.fetchall():
        print(i)

@connector
def del_table(conn):
    """"Видаляємо таблицю в базі даних"""

    sql_text = "DROP TABLE product"

    c = conn.cursor()
    c.execute(sql_text)


@connector
def table(conn):
    """Перелік таблиць в базі даних
    Виводимо список в консоль"""

    sql_text = """SELECT  name FROM  sqlite_master """

    c = conn.cursor()
    c.execute(sql_text)

    for i in c.fetchall():
        print(i)


if __name__ == '__main__':
    create_table(create_table_product)
    create_table(create_table_sales)
    #insert_product('test', 'r')
    #select_product()
