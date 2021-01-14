def get_add_flight_query(code, time, start_city, target_city, ticket_price,
                         airplane_code, captain_code):
    query = 'INSERT INTO TRAVEL (code, time, startCity, targetCity, ticketPrice,' \
            'airplaneCode, captainCode) VALUES("' + code + '", "' + time + '", "' + start_city + '", "' +\
            target_city + '", ' + str(ticket_price) + ', "' + airplane_code + '", "' + captain_code + '");'
    return query


def get_all_flight_query():
    query = '''SELECT * FROM TRAVEL;'''
    return query


def get_all_airplanes_query():
    query = '''SELECT * FROM AIRPLANE;'''
    return query


def get_add_airplane_query(code, capacity, model, city):
    query = '''INSERT INTO AIRPLANE (code, capacity, model, city) VALUES'''
    query += '("' + code + '", ' + str(capacity) + ', "' + model + '", "' + city + '");'
    return query


def get_remove_airplane_query(code):
    query = '''DELETE FROM AIRPLANE WHERE code = ''' + '"' + code + '";'
    return query


def get_all_comments_query():
    query = '''SELECT * FROM COMMENT;'''
    return query


def get_all_employees_query():
    query = '''SELECT * FROM EMPLOYEE;'''
    return query


def get_all_travels_query():
    query = '''SELECT * FROM TRAVEL;'''
    return query


def get_customers_by_travels():
    query = '''SELECT X.nc, X.firstName, X.lastName, count(*)
                FROM CUSTOMER as X, ORDER_TABLE as Y
                WHERE Y.customerNC = X.nc
                GROUP BY X.nc, X.firstName, X.lastName
                ORDER BY count(*) DESC;'''
    return query


def get_add_discount_query(nc, discount_no, percent, expiration_time):
    query = '''INSERT INTO DISCOUNT (customerNC, discountNo, percent, 
                expirationTime, orderNo, customerOrderNC) VALUES '''
    query += '("' + nc + '", "' + discount_no + '", ' + str(percent) + \
             ', "' + expiration_time + '", null, null);'
    return query


def get_all_customers_query():
    query = '''SELECT * FROM CUSTOMER;'''
    return query


def get_target_city_query():
    query = '''SELECT targetCity, count(*) FROM TRAVEL
            GROUP BY targetCity
            ORDER BY count(*) DESC;'''
    return query


def get_airplanes_in_city_query(city):
    query = '''SELECT * FROM AIRPlANE WHERE city = ''' + '"' + city + '";'
    return query


def get_give_salary_query():
    query = '''UPDATE EMPLOYEE SET totalSalary = totalSalary + salary;'''
    return query


def get_employee_score_query():
    query = '''SELECT * from CrewScoreMView;'''
    return query


def get_airplane_score_query():
    query = '''SELECT * FROM AirplaneScoreMView;'''
    return query


def get_captains_score_query():
    query = '''SELECT * FROM CaptainScoreMView;'''
    return query


def get_insert_employee_query(code, name, job_type, year, salary, total_salary):
    query = 'INSERT INTO EMPLOYEE VALUES ("' + code + '", "' + name + '", "' + \
            job_type + '", "' + year + '", ' + str(salary) + ', ' + str(total_salary) + ');'
    return query


def get_insert_flight_crew_query(travel_code, employee_code):
    query = 'INSERT INTO FLIGHT_CREW VALUES ("' + employee_code + '", "' + travel_code + '");'
    return query


def get_remove_unpaid_orders_query(travel_code):
    query = 'DELETE FROM ORDER_TABLE WHERE travelCode = "' + travel_code +\
            '" and paymentStatus = "NotPaid"'
    return query


def get_change_airplane_city_query(code, city):
    query = 'UPDATE AIRPLANE SET city = "' + city + '" WHERE code = "' + code + '";'
    return query


if __name__ == '__main__':
    print(get_add_flight_query('10', '2021/10/02', 'tehran', 'mashahd', 10, '1', '1'))
    print(get_add_discount_query('10', '10', 70, '2010/10/10'))
    print(get_remove_airplane_query('10'))
    print(get_add_airplane_query('100', 100, 'Boeing 747', 'Tehran'))
    print(get_target_city_query())
    print(get_airplanes_in_city_query('Tehran'))
    print(get_give_salary_query())
    print(get_all_employees_query())
    print(get_all_travels_query())
    print(get_all_customers_query())
    print(get_all_airplanes_query())
    print(get_customers_by_travels())
    print(get_captains_score_query())
    print(get_insert_employee_query('1010', 'Keivan', 'Cap', '2020', 1000, 0))
    print(get_insert_flight_crew_query('100', '1000'))
    print(get_remove_unpaid_orders_query('100'))
    print(get_change_airplane_city_query('10', '1000'))
