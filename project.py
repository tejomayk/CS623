import psycopg2
from psycopg2 import sql

db_params = {
    "dbname": "test",
    "user": "postgres",
    "password": "9797",
    "host": "localhost",
}

def execute_transaction(queries):
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    try:
        connection.autocommit = False
        connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)

        for query in queries:
            cursor.execute(sql.SQL(query))

        connection.commit()
        print("Transaction succeeded!")

    except Exception as e:
        connection.rollback()
        print(f"Transaction failed: {e}")

    finally:
        cursor.close()
        connection.close()


transaction_statements = [
    "DELETE FROM stock WHERE prod_id='p1';",
    "DELETE FROM product WHERE prod_id='p1';",
    "DELETE FROM stock WHERE dep_id='d1';",
    "DELETE FROM depot WHERE dep_id='d1';",
    "INSERT INTO product (prod_id,pname,price) VALUES('p100','cd',5);",
    "INSERT INTO stock (prod_id,dep_id,quantity) VALUES('p100','d2',50);",
    "INSERT INTO depot (dep_id,addr,volume) VALUES('d100','Chicago',100);",
    "INSERT INTO product (prod_id,pname,price) VALUES('p1','tape',2.50);",
    "INSERT INTO stock (prod_id,dep_id,quantity) VALUES('p1','d100',100);",
]


execute_transaction(transaction_statements)