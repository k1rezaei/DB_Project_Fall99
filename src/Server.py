import psycopg2
from psycopg2 import Error
from Login import my_database, my_password
from Terminal.Terminal import Terminal

if __name__ == '__main__':
    try:
        connection = psycopg2.connect(user="postgres",
                                      password=my_password,
                                      host="127.0.0.1",
                                      database=my_database)
        cursor = connection.cursor()

        terminal = Terminal(cursor)
        terminal.start()

        '''# Print PostgreSQL details
        print("PostgreSQL server information")
        print(connection.get_dsn_parameters(), "\n")
        cursor.execute("SELECT version();")
        # Fetch result
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")'''

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
