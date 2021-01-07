import psycopg2
from psycopg2 import Error


def execute_create_query(cursor, query, table_name):
    try:
        cursor.execute(query)
    except (Exception, Error) as error:
        print("Error While Creating " + table_name, error)


def create_customer(cursor):
    query = 'CREATE TABLE CUSTOMER(' \
            'NC varchar(10),firstName varchar(15),' \
            'lastName varchar(15), money real,' \
            'primary key (NC));'
    execute_create_query(cursor, query, 'CUSTOMER')


def create_comment(cursor):
    query = 'CREATE TABLE COMMENT(' \
            'customerNC varchar(10),commentNO varchar(10),text varchar,' \
            'primary key (customerNC, commentNo),' \
            'foreign key (customerNC) references CUSTOMER(NC));'
    execute_create_query(cursor, query, 'COMMENT')


def create_employee(cursor):
    query = 'CREATE TABLE EMPLOYEE(' \
            'code varchar(10), name varchar(20), jobType varchar(10),' \
            'employment_year varchar(4), salary real, totalSalary real,' \
            'primary key (code));'
    execute_create_query(cursor, query, 'EMPLOYEE')


def create_travel(cursor):
    query = 'CREATE TABLE TRAVEL(' \
            'code varchar(10), time timestamp, ' \
            'startCity varchar(10), targetCity varchar(10), ticketPrice real, ' \
            'airplaneCode varchar(10), captainCode varchar (10),' \
            'primary key (code),' \
            'foreign key(airplaneCode) references AIRPLANE(code),' \
            'foreign key (captainCode) references EMPLOYEE(code));'
    execute_create_query(cursor, query, 'TRAVEL')


def create_flight_crew(cursor):
    query = 'CREATE TABLE FLIGHT_CREW(' \
            'employeeCode varchar(10), travelCode varchar(10),' \
            'primary key(employeeCode, travelCode),' \
            'foreign key (employeeCode) references EMPLOYEE(code),' \
            'foreign key (travelCode) references TRAVEL(code));'
    execute_create_query(cursor, query, 'FLIGHT_CREW')
