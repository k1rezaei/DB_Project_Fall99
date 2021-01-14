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
    #cursor.execute("CREATE USER customer_user WITH PASSWORD 'userpass';")
    cursor.execute('''
            GRANT ALL PRIVILEGES ON CUSTOMER TO customer_user;
            GRANT ALL PRIVILEGES ON COMMENT TO customer_user;
            GRANT ALL PRIVILEGES ON DISCOUNT TO customer_user;
            GRANT ALL PRIVILEGES ON ORDER_TABLE TO customer_user;
            GRANT ALL PRIVILEGES ON TRAVEL TO customer_user;
            GRANT ALL PRIVILEGES ON AirplaneScoreUView TO customer_user;
            GRANT ALL PRIVILEGES ON TravelEmptySeatUView TO customer_user;
        ''')


def triggers(cursor):
    insert_travel_time = '''
    CREATE OR REPLACE FUNCTION travel_time_check()
    RETURNS TRIGGER 
    LANGUAGE PLPGSQL
    AS
    $$
    BEGIN
    IF NEW.time < clock_timestamp() THEN
        RAISE EXCEPTION 'cannot insert expired flight';
    END IF;
    RETURN NEW;
    END;
    $$;
    CREATE TRIGGER insert_travel_time BEFORE INSERT ON TRAVEL
        FOR EACH ROW
        EXECUTE PROCEDURE travel_time_check();
    '''

    insert_travel_captain = '''
    CREATE OR REPLACE FUNCTION travel_captain_check()
    RETURNS TRIGGER 
    LANGUAGE PLPGSQL
    AS
    $$
    BEGIN
    IF NOT NEW.captainCode IN (SELECT code FROM EMPLOYEE WHERE jobType = 'Captain') THEN
        RAISE EXCEPTION 'captain is not valid';
    END IF;
    RETURN NEW;
    END;
    $$;
    CREATE TRIGGER insert_travel_captain BEFORE INSERT ON TRAVEL
        FOR EACH ROW
        EXECUTE PROCEDURE travel_captain_check();
    '''

    insert_flight_crew = '''
    CREATE OR REPLACE FUNCTION flight_crew_time_check()
    RETURNS TRIGGER 
    LANGUAGE PLPGSQL
    AS
    $$
    BEGIN
    IF clock_timestamp() > ALL(SELECT time FROM TRAVEL where code=NEW.travelCode) THEN
        RAISE EXCEPTION 'flight is passed, cannot add crew';
    END IF;
    RETURN NEW;
    END;
    $$;
    CREATE TRIGGER insert_flight_crew BEFORE INSERT ON FLIGHT_CREW
        FOR EACH ROW
        EXECUTE PROCEDURE flight_crew_time_check();
    '''

    insert_discount = '''
    CREATE OR REPLACE FUNCTION discount_time()
    RETURNS TRIGGER 
    LANGUAGE PLPGSQL
    AS
    $$
    BEGIN
    IF clock_timestamp() > NEW.expirationTime THEN
        RAISE EXCEPTION 'cannot give expired discount!';
    END IF;
    RETURN NEW;
    END;
    $$;
    CREATE TRIGGER insert_discount BEFORE INSERT ON DISCOUNT
        FOR EACH ROW
        EXECUTE PROCEDURE discount_time();
    '''

    increasing_total_salary = '''
    CREATE OR REPLACE FUNCTION total_salary_increasing()
    RETURNS TRIGGER 
    LANGUAGE PLPGSQL
    AS
    $$
    BEGIN
    IF NEW.totalSalary < OLD.totalSalary THEN
        RAISE EXCEPTION 'salary is decreasing!';
    END IF;
    RETURN NEW;
    END;
    $$;
    CREATE TRIGGER increasing_total_salary BEFORE UPDATE OF totalSalary ON EMPLOYEE
        FOR EACH ROW
        EXECUTE PROCEDURE total_salary_increasing();
    '''

    insert_travel_airplane_city = '''
    CREATE OR REPLACE FUNCTION travel_airplane_city()
    RETURNS TRIGGER 
    LANGUAGE PLPGSQL
    AS
    $$
    BEGIN
    IF NEW.startCity != (SELECT city FROM AIRPLANE WHERE NEW.airplaneCode = code) THEN
        RAISE EXCEPTION 'airplane is not in start city!';
    END IF;
    RETURN NEW;
    END;
    $$;
    CREATE TRIGGER insert_travel_airplane_city BEFORE INSERT ON TRAVEL
        FOR EACH ROW
        EXECUTE PROCEDURE travel_airplane_city();
    '''

    cursor.execute(insert_travel_time)
    cursor.execute(insert_travel_captain)
    cursor.execute(insert_flight_crew)
    cursor.execute(insert_discount)
    cursor.execute(increasing_total_salary)
    cursor.execute(insert_travel_airplane_city)


def insert(cursor):
    cursor.execute('''
        insert into airplane values('0', 3, 'EF715', 'Munikh');
        insert into airplane values('1', 3, 'EF717', 'NewYork');
        insert into airplane values('2', 3, 'EF718', 'NewYork');
        insert into airplane values('3', 3, 'EF206', 'Tehran');
        insert into airplane values('4', 3, 'EH718', 'Istanbul');

        insert into seat values('0', '0');
        insert into seat values('1', '0');
        insert into seat values('2', '0');

        insert into seat values('0', '1');
        insert into seat values('1', '1');
        insert into seat values('2', '1');

        insert into seat values('0', '2');
        insert into seat values('1', '2');
        insert into seat values('2', '2');

        insert into seat values('0', '3');
        insert into seat values('1', '3');
        insert into seat values('2', '3');

        insert into seat values('0', '4');
        insert into seat values('1', '4');
        insert into seat values('2', '4');

        insert into employee values('0', 'Ahmad Ahmadi', 'Captain', '2018', 1500, 15000);
        insert into employee values('1', 'Ali Alavi', 'Captain', '2019', 1000, 10000);
        insert into employee values('2', 'Reza Razavi', 'Technician', '2020', 300, 900);
        insert into employee values('3', 'Hasan Hasani', 'Crew', '2019', 100, 1000);
        insert into employee values('4', 'Sima Bina', 'Crew', '2019', 100, 1500);
        insert into employee values('5', 'Mahmood Tajik', 'Crew', '2019', 100, 1000);
        
        insert into travel values('0', '2021-01-12 01:45:00', 'Tehran', 'Mashhad', 100, '0', '0');
        insert into travel values('1', '2021-01-10 01:35:00', 'Tehran', 'Ahvaz', 500, '1', '1');
        insert into travel values('2', '2021-01-20 02:35:00', 'Ahvaz', 'Mashhad', 200, '1', '0');
        insert into travel values('3', '2021-01-10 16:35:00', 'Mashhad', 'Tehran', 60, '2', '1');

        insert into flight_crew values('2', '0');
        insert into flight_crew values('2', '1');
        insert into flight_crew values('2', '2');
                
        insert into flight_crew values('3', '1');
        insert into flight_crew values('3', '2');

        insert into flight_crew values('4', '0');
        insert into flight_crew values('4', '3');
        
        insert into flight_crew values('5', '0');
        insert into flight_crew values('5', '1');
        insert into flight_crew values('5', '2');
        

        insert into customer values('100', '123', 'Shayan', 'Hosseini', 50);
        insert into customer values('101', '123', 'Mohammad', 'Shafiee', 10);
        insert into customer values('102', '123', 'Tooraj', 'Falsafi', 100);

        insert into comment values('100', '1', 'Perfect Flights!');
        insert into comment values('101', '2', 'Awful Airplane!');

        insert into discount values('100', '1', 90, '2021-02-21 16:35:00', null);
        insert into discount values('100', '2', 91, '2020-02-21 16:35:00', null);
        insert into discount values('101', '1', 84, '2021-02-21 16:35:00', null);
        insert into discount values('101', '2', 95, '2021-02-21 16:35:00', null);
        insert into discount values('102', '1', 70, '2021-02-21 16:35:00', null);
        
        insert into order_table values('100', '0', 'Paid','0', 100, '0', '0');
        insert into order_table values('100', '1', 'Paid','0', 80, '1', '0');
        insert into order_table values('101', '0', 'Paid','0', 70, '2', '0');
        
        insert into order_table values('101', '1', 'Paid','1', 60, '0', '1');
        insert into order_table values('102', '0', 'Paid','1', 100, '1', '1');
        insert into order_table values('102', '1', 'Paid','1', 50, '2', '1');
        
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

        user_view.drop_all()
        manager_view.drop_all()
        drop_tables(cursor)

        create_tables(cursor)
        user_view.create_all()
        manager_view.create_all()
        create_user(cursor)
        insert(cursor)
        triggers(cursor)

        connection.commit()

    except (Exception, Error) as error:
        print("Error while connecting manager to PostgreSQL", error)


