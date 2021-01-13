import psycopg2
from psycopg2 import Error
from Login import my_database, user_password, manager_password, user_username, manager_username
from Terminal.Terminal import Terminal
from Terminal.ManagerTerminal import ManagerTerminal
if __name__ == '__main__':
    try:
        connection = psycopg2.connect(user=user_username,
                                      password=user_password,
                                      host="127.0.0.1",
                                      database=my_database)
        cursor = connection.cursor()

        terminal = Terminal(cursor)
        terminal.start()

    except (Exception, Error) as error:
        print("Error while connecting manager to PostgreSQL", error)
