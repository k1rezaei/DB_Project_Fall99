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
    # cursor.execute("CREATE USER customer_user WITH PASSWORD 'userpass';")
    cursor.execute('''
            GRANT ALL PRIVILEGES ON CUSTOMER TO customer_user;
            GRANT ALL PRIVILEGES ON COMMENT TO customer_user;
            GRANT ALL PRIVILEGES ON DISCOUNT TO customer_user;
            GRANT ALL PRIVILEGES ON ORDER_TABLE TO customer_user;
            GRANT ALL PRIVILEGES ON TRAVEL TO customer_user;
            GRANT ALL PRIVILEGES ON AirplaneScoreUView TO customer_user;
            GRANT ALL PRIVILEGES ON TravelEmptySeatUView TO customer_user;
        ''')


def insert(connection, cursor):
    cursor.execute('''
        insert into airplane values('210', 3, 'EF715', 'Munikh');
        insert into airplane values('211', 3, 'EF717', 'NewYork');
        insert into airplane values('212', 3, 'EF718', 'NewYork');
        insert into airplane values('213', 3, 'EF206', 'Tehran');
        insert into airplane values('214', 3, 'EH718', 'Istanbul');

        insert into seat values('100', '210');
        insert into seat values('101', '210');
        insert into seat values('102', '210');

        insert into seat values('100', '211');
        insert into seat values('101', '211');
        insert into seat values('102', '211');

        insert into seat values('100', '212');
        insert into seat values('101', '212');
        insert into seat values('102', '212');

        insert into seat values('100', '213');
        insert into seat values('101', '213');
        insert into seat values('102', '213');

        insert into seat values('100', '214');
        insert into seat values('101', '214');
        insert into seat values('102', '214');

        insert into employee values('123', 'Seyed', 'Captain', '1396', 1500, 0);
        insert into employee values('124', 'Keivan', 'Captain', '1396', 1000, 0);
        insert into employee values('125', 'Hasan Agha', 'Mehmandar', '1396', 100, 0);
        insert into employee values('126', 'Mina', 'Mehmandar', '1396', 100, 0);

        insert into travel values('100', '2020-02-21 01:45:00', 'Tehran', 'Mashhad', 6, '210', '123');
        insert into travel values('101', '2021-02-21 01:35:00', 'Tehran', 'Mashhad', 7, '213', '123');
        insert into travel values('102', '2021-02-21 02:35:00', 'Tehran', 'Mashhad', 8, '212', '124');
        insert into travel values('103', '2021-02-21 16:35:00', 'Mashhad', 'Tehran', 5, '210', '124');

        insert into flight_crew values('125', '100');
        insert into flight_crew values('125', '101');
        insert into flight_crew values('126', '102');
        insert into flight_crew values('125', '103');

        insert into customer values('102', '123', 'Shayan', 'ttt', 0);
        insert into customer values('103', '123', 'Hasan', 'sss', 10);
        insert into customer values('104', '123', 'Ray', 'rrr', 10);

        insert into comment values('102', '1', 'Che vazeshe agha havapeymatoon booye goh mide,\n zire sandalia adams chasbide\n mehmandara ba capitan mafia bazi mikonan :/');
        insert into comment values('103', '2', 'Chahe dastshooyi havapeymaye EF206 gerefte!');

        insert into discount values('102', '1', 90, '2021-02-21 16:35:00', null, null);
        insert into discount values('102', '2', 91, '2020-02-21 16:35:00', null, null);
        insert into discount values('102', '3', 84, '2021-02-21 16:35:00', null, null);
        insert into discount values('102', '4', 95, '2021-02-21 16:35:00', null, null);
        insert into discount values('102', '5', 70, '2021-02-21 16:35:00', null, null);
    ''')

    connection.commit()


if __name__ == '__main__':
    try:
        connection = psycopg2.connect(user=manager_username,
                                      password=manager_password,
                                      host="127.0.0.1",
                                      database=my_database)
        cursor = connection.cursor()
        insert(connection, cursor)
        """
        user_view = UserView(cursor)
        manager_view = ManagerView(cursor)

        user_view.drop_all()
        manager_view.drop_all()
        #drop_tables(cursor)'

        #create_tables(cursor)
        user_view.create_all()
        manager_view.create_all()
        create_user(cursor)
        """
        connection.commit()

    except (Exception, Error) as error:
        print("Error while connecting manager to PostgreSQL", error)


