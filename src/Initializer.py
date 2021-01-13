import psycopg2
from psycopg2 import Error

from Queries import ManagerQueries
from Definer.TableDefiner import create_tables, drop_tables
from Definer.ViewDefiner import UserView, ManagerView
from Login import my_database, user_password, manager_password, user_username, manager_username
from Terminal.Terminal import Terminal
from Terminal.ManagerTerminal import ManagerTerminal


def delete_user(cursor):
    cursor.execute("DROP USER customer_user;")


def create_user(cursor):
    cursor.execute("CREATE USER customer_user WITH PASSWORD 'userpass';")
    cursor.execute('''
            GRANT ALL PRIVILEGES ON CUSTOMER TO customer_user;
            GRANT ALL PRIVILEGES ON COMMENT TO customer_user;
            GRANT ALL PRIVILEGES ON DISCOUNT TO customer_user;
            GRANT ALL PRIVILEGES ON ORDER_TABLE TO customer_user;
            GRANT ALL PRIVILEGES ON TRAVEL TO customer_user;
            GRANT ALL PRIVILEGES ON AirplaneScoreUView TO customer_user;
            GRANT ALL PRIVILEGES ON TravelEmptySeatUView TO customer_user;
        ''')


if __name__ == '__main__':
    try:
        connection = psycopg2.connect(user=manager_username,
                                      password=manager_password,
                                      host="127.0.0.1",
                                      database=my_database)
        cursor = connection.cursor()

        user_view = UserView(cursor)
        manager_view = ManagerView(cursor)

        '''user_view.drop_all()
        manager_view.drop_all()
        drop_tables(cursor)'''

        create_tables(cursor)
        user_view.create_all()
        manager_view.create_all()
        create_user(cursor)

        connection.commit()

    except (Exception, Error) as error:
        print("Error while connecting manager to PostgreSQL", error)
