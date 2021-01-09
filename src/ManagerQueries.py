def get_add_flight_query(code, time, start_city, target_city, ticket_price,
                         airplane_code, captain_code):
    query = '''INSERT INTO TRAVEL (code, time, startCity, targetCity, ticketPrice,
     airplaneCode, captainCode) VALUES'''
    query += '(' + code + ',' + time + ',' + start_city + ',' + target_city + ','
    query += ticket_price + ',' + airplane_code + ',' + captain_code + ');'
    return query


def get_all_flight_query():
    query = '''SELECT * FROM TRAVEL'''
    return query


def get_all_airplanes_query():
    query = '''SELECT * FROM AIRPLANE'''
    return query


def get_add_airplane_query(code, capacity, model, city):
    query = '''INSERT INTO AIRPLANE (code, capacity, model, city) VALUES'''
    query += '(' + code + ',' + capacity + ',' + model + ',' + city + ');'
    return query


def get_remove_airplane_query(code):
    query = '''DELETE FROM AIRPLANE WHERE code = ''' + code + ';'
    return query


def get_all_comments_query():
    query = '''SELECT * FROM COMMENTS'''
    return query

