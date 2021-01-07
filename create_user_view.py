import psycopg2
from psycopg2 import Error


def execute_create_view_query(cursor, query, view_name):
    try:
        cursor.execute(query)
    except (Exception, Error) as error:
        print("Error While Creating(View) " + view_name, error)


def create_view_customer(cursor):
    query = 'CREATE VIEW vCustomer (NC, firstName, lastName, money)' \
            'AS SELECT * FROM CUSTOMER;'
    execute_create_view_query(cursor, query, 'CUSTOMER')


def create_view_comment(cursor):
    query = 'CREATE VIEW vComment (customerNC, commentNo, text)' \
            'AS SELECT * FROM COMMENT;'
    execute_create_view_query(cursor, query, 'COMMENT')


def create_view_discount(cursor):  # TODO
    pass


def create_view_order(cursor):  # TODO
    pass


def create_view_travel(cursor):
    query = 'CREATE VIEW vTravel code, time, startCity, targetCity, ' \
            'ticketPrice, airplaneCode, captainCode' \
            'AS SELECT * FROM TRAVEL;'
    execute_create_view_query(cursor, query, 'TRAVEL')


def create_view_airplane_score(cursor):  # TODO
    pass


def create_view_travel_empty_seat(cursor):  # TODO
    pass
