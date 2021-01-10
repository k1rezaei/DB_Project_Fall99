def get_add_flight_query(code, time, start_city, target_city, ticket_price,
                         airplane_code, captain_code):
    query = '''INSERT INTO TRAVEL (code, time, startCity, targetCity, ticketPrice,
     airplaneCode, captainCode) VALUES'''
    query += '("' + code + '", "' + time + '", "' + start_city + '", "' + target_city + '", '
    query += str(ticket_price) + ', "' + airplane_code + '", "' + captain_code + '");'
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
    query = '''SELECT * FROM COMMENTS;'''
    return query


def get_add_discount_query(nc, discount_no, percent, expiration_time):
    query = '''INSERT INTO DISCOUNT (customerNC, discountNo, percent, 
                expirationTime, orderNo, customerOrderNC) VALUES '''
    query += '("' + nc + '", "' + discount_no + '", ' + str(percent) +\
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

# TODO: change query tables, to view tables! IMPORTANT


if __name__ == '__main__':
    print(get_add_flight_query('10', '2021/10/02', 'tehran', 'mashahd', 10, '1', '1'))
    print(get_add_discount_query('10', '10', 70, '2010/10/10'))
    print(get_remove_airplane_query('10'))
    print(get_add_airplane_query('100', 100, 'Boeing 747', 'Tehran'))
    print(get_target_city_query())
    print(get_airplanes_in_city_query('Tehran'))
    print(get_give_salary_query())
