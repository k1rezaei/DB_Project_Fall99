import psycopg2
from psycopg2 import Error
from Login import my_database, my_password

if __name__ == '__main__':
    print("hello world")
    try:
        connection = psycopg2.connect(user="postgres",
                                      password=my_password,
                                      host="127.0.0.1",
                                      database=my_database)
        cursor = connection.cursor()
        # Print PostgreSQL details
        print("PostgreSQL server information")
        print(connection.get_dsn_parameters(), "\n")
        cursor.execute("SELECT version();")
        # Fetch result
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)

    print(10)
