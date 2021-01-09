import psycopg2
from psycopg2 import Error


class UserView:
    def __init__(self, cursor):
        self.cursor = cursor

    def execute_create_view_query(self, query, view_name):
        try:
            self.cursor.execute(query)
        except (Exception, Error) as error:
            print("Error While Creating(View) " + view_name, error)

    def create_view_customer(self):
        query = 'CREATE VIEW vCustomer (NC, firstName, lastName, money)' \
                'AS SELECT * FROM CUSTOMER;'
        self.execute_create_view_query(query, 'CUSTOMER')

    def create_view_comment(self):
        query = 'CREATE VIEW vComment (customerNC, commentNo, text)' \
                'AS SELECT * FROM COMMENT;'
        self.execute_create_view_query(query, 'COMMENT')

    def create_view_discount(self):  # TODO
        pass

    def create_view_order(self):  # TODO
        pass

    def create_view_travel(self):
        query = 'CREATE VIEW vTravel code, time, startCity, targetCity, ' \
                'ticketPrice, airplaneCode, captainCode' \
                'AS SELECT * FROM TRAVEL;'
        self.execute_create_view_query(self, query, 'TRAVEL')

    def create_view_airplane_score(self):  # TODO
        pass

    def create_view_travel_empty_seat(self):  # TODO
        pass


class ManagerView:
    def __init__(self, cursor):
        self.cursor = cursor
