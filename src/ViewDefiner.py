import psycopg2
from psycopg2 import Error


class ViewDefiner:
    def __init__(self, cursor):
        self.cursor = cursor

    def execute_create_view_query(self, query, view_name):
        try:
            self.cursor.execute(query)
        except (Exception, Error) as error:
            print("Error While Creating(View) " + view_name, error)


class UserView(ViewDefiner):
    def create_view_customer(self):
        query = '''CREATE VIEW CustomerUView (NC, firstName, lastName, money)
                    AS SELECT * FROM CUSTOMER;'''
        self.execute_create_view_query(query, 'CustomerUView')

    def create_view_comment(self):
        query = '''CREATE VIEW CommentUView (customerNC, commentNo, text)
                    AS SELECT * FROM COMMENT;'''
        self.execute_create_view_query(query, 'CommentUView')

    def create_view_discount(self):
        query = '''CREATE VIEW DiscountUView (customerNC, discountNo, percent,
                    expirationTime, orderNo, customerOrderNC)
                    AS SELECT * FROM DISCOUNT'''
        self.execute_create_view_query(query, 'DiscountUView')

    def create_view_order(self):
        query = '''CREATE VIEW OrderUView (customerNC, orderNo, paymentStatus,
                            travelCode, score, seatNo, airplaneCode)
                            AS SELECT * FROM ORDER'''
        self.execute_create_view_query(query, 'OrderUView')

    def create_view_travel(self):
        query = '''CREATE VIEW TravelUView (code, time, startCity, targetCity, 
                    ticketPrice, airplaneCode, captainCode)
                    AS SELECT * FROM TRAVEL;'''
        self.execute_create_view_query(query, 'TravelUView')

    def create_view_airplane_score(self):
        query = '''CREATE VIEW AirplaneScoreUView (airplaneCode, avgScore)
                    AS SELECT A.code, AVG(O.score) FROM AIRPLANE AS A, ORDER AS O
                    WHERE A.code = O.airplaneCode
                    GROUP BY A.code;
                '''
        self.execute_create_view_query(query, 'AirplaneScoreUView')

    def create_view_travel_empty_seat(self):
        query = '''CREATE VIEW TravelEmptySeatUView (travelCode, seatNo, airplaneCode)
                    AS ((SELECT T.code AS travelCode, A.seatNo AS seatNo, A.airplaneCode AS airplaneCode
                        FROM TRAVEL AS T, AIRPLANE AS A 
                        WHERE T.airplaneCode = A.code)
                        except
                        (SELECT travelCode, seatNo, airplaneCode FROM ORDER));
                '''
        self.execute_create_view_query(query, 'TravelEmptySeatUView')


class ManagerView(ViewDefiner):
    def create_view_customer(self):
        query = '''CREATE VIEW CustomerMView (NC, firstName, lastName, money)
                    AS SELECT * FROM CUSTOMER;'''
        self.execute_create_view_query(query, 'CustomerMView')

    def create_view_comment(self):
        query = '''CREATE VIEW CommentMView (customerNC, commentNo, text)
                    AS SELECT * FROM COMMENT;'''
        self.execute_create_view_query(query, 'CommentMView')

    def create_view_discount(self):
        query = '''CREATE VIEW DiscountMView (customerNC, discountNo, percent, expirationTime, orderNo, customerOrderNo)
                    AS SELECT * FROM DISCOUNT;'''
        self.execute_create_view_query(query, 'DiscountMView')

    def create_view_airplane(self):
        query = '''CREATE VIEW AirplaneMView (code, seatNo)
                    AS SELECT * FROM AIRPLANE;'''
        self.execute_create_view_query(query, 'AirplaneMView')

    def create_view_employee(self):
        query = '''CREATE VIEW EmployeeMView (code, name, jobType,
                    employmentYear, salary, totalSalary)
                    AS SELECT * FROM EMPLOYEE;'''
        self.execute_create_view_query(query, 'EmployeeMView')

    def create_view_seat(self):
        query = '''CREATE VIEW SeatMView (airplaneCode, seatNo)
                    AS SELECT * FROM SEAT;'''
        self.execute_create_view_query(query, 'SeatMView')

    def create_view_order(self):
        query = '''CREATE VIEW OrderMView (customerNC, orderNo, paymentStatus, 
                    travelCode, score, seatNo, airplaneCode)
                    AS SELECT * FROM ORDER;'''
        self.execute_create_view_query(query, 'OrderMView')

    def create_view_travel(self):
        query = '''CREATE VIEW TravelMView (code, time, startCity, targetCity,
                    ticketPrice, airplaneCode, captainCode)
                    AS SELECT * FROM TRAVEL;'''
        self.execute_create_view_query(query, 'TravelMView')

    def create_view_flight_crew(self):
        query = '''CREATE VIEW FlightCrewMView (employeeCode, travelCode)
                    AS SELECT * FROM FLIGHT_CREW;'''
        self.execute_create_view_query(query, 'TravelMView')

