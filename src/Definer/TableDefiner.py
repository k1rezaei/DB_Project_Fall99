import psycopg2
from psycopg2 import Error


def execute_create_table_query(cursor, query, table_name):
    try:
        cursor.execute(query)
    except (Exception, Error) as error:
        print("Error While Creating(Table) " + table_name, error)


def create_customer(cursor):
    query = '''CREATE TABLE CUSTOMER(
                NC varchar(10),firstName varchar(15),
                lastName varchar(15), money real NOT NULL,
                CHECK (money >= 0),
                primary key (NC));'''
    execute_create_table_query(cursor, query, 'CUSTOMER')


def create_comment(cursor):
    query = '''CREATE TABLE COMMENT(
                customerNC varchar(10),commentNO varchar(10),text varchar(300),
                primary key (customerNC, commentNo),
                foreign key (customerNC) references CUSTOMER(NC));'''
    execute_create_table_query(cursor, query, 'COMMENT')


def create_employee(cursor):
    query = '''CREATE TABLE EMPLOYEE(
            code varchar(10), name varchar(20), jobType varchar(10),
            employmentYear varchar(4), salary real NOT NULL, totalSalary real NOT NULL,
            CHECK (salary >= 0),
            CHECK (totalSalary >= 0),
            primary key (code));'''
    execute_create_table_query(cursor, query, 'EMPLOYEE')


def create_travel(cursor):
    query = '''CREATE TABLE TRAVEL(
                code varchar(10), time timestamp NOT NULL,
                startCity varchar(10) NOT NULL, targetCity varchar(10) NOT NULL, ticketPrice real NOT NULL,
                airplaneCode varchar(10) NOT NULL, captainCode varchar (10) NOT NULL,
                CHECK (ticketPrice >= 0),
                primary key (code),
                foreign key(airplaneCode) references AIRPLANE(code),
                foreign key (captainCode) references EMPLOYEE(code));'''
    execute_create_table_query(cursor, query, 'TRAVEL')


def create_flight_crew(cursor):
    query = '''CREATE TABLE FLIGHT_CREW(
                employeeCode varchar(10), travelCode varchar(10),
                primary key(employeeCode, travelCode),
                foreign key (employeeCode) references EMPLOYEE(code),
                foreign key (travelCode) references TRAVEL(code));'''
    execute_create_table_query(cursor, query, 'FLIGHT_CREW')


def create_discount(cursor):
    query = '''CREATE TABLE DISCOUNT(
            customerNC varchar(10), discountNo varchar(10), 
            percent real NOT NULL, expirationTime timestamp NOT NULL,
            orderNo varchar(10), customerOrderNC varchar (10),
            primary key (customerNC, discountNo),
            foreign key (customerNC) references CUSTOMER(NC),
            foreign key (orderNo, customerOrderNC) references ORDER(orderNo, customerNC));'''
    execute_create_table_query(cursor, query, 'DISCOUNT')


def create_airplane(cursor):
    query = '''CREATE TABLE AIRPLANE(
                code varchar(10),
                capacity integer NOT NULL,
                model varchar(10) NOT NULL,
                city varchar(10),
                check ( capacity > 0 ),
                primary key (code));'''
    execute_create_table_query(cursor, query, 'AIRPLANE')


def create_seat(cursor):
    query = '''CREATE TABLE SEAT(
                seatNo varchar(10),
                airplaneCode varchar(10),
                primary key (airplaneCode, seatNo),
                foreign key (airplaneCode) references AIRPLANE(code));'''
    execute_create_table_query(cursor, query, 'SEAT')


def create_order(cursor):
    query = '''CREATE TABLE ORDER(
                customerNC varchar(10), orderNo varchar(10), 
                paymentStatus varchar(10) NOT NULL, travelCode varchar(10),
                score real, seatNo varchar(10),
                airplaneCode varchar(10),
                check ( score >= 0 ),
                check ( paymentStatus in('Paid','NotPaid') ),
                primary key (customerNC, orderNo),
                foreign key (customerNC) references CUSTOMER(NC),
                foreign key (travelCode) references TRAVEL(code),
                foreign key (airplaneCode, seatNo) references SEAT(airplaneCode,seatNo));'''
    execute_create_table_query(cursor, query, 'ORDER')


def create_account(cursor):
    query = '''CREATE TABLE ACCOUNT(
                    username varchar(10) not null, password varchar(10) not null, isManager boolean not null,
                    primary key (username),
                    foreign key (customerNC) references CUSTOMER(NC));'''
    execute_create_table_query(cursor, query, 'ORDER')