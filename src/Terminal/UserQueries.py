def query_discount_set_null(order_no, travel_code):
    return '''
                update DISCOUNT 
                set orderNo = null, customerOrderNC = null
                where travelCode = "''' + travel_code + '''"
                and orderNo = "''' + order_no + '''"
                ;
            '''


def query_all_future_flights():
    # attention: don't put semicolon at the end of this query
    return '''
        select *, (select count(*)
                    from TravelEmptySeatUView as ES 
                    where T.code=ES.travelCode
        ) as emptySeats
        from TRAVEL as T, AirplaneScoreUView as AirS
        where clock_timestamp() < T.time
        and T.airplaneCode = AirS.airplaneCode
        '''


def query_travel_price(travel_code):
    return '''
                select price 
                from TRAVEL 
                where code = "''' + travel_code + '''"
            '''


def query_empty_seats(travel_code):
    return '''
            select airplaneCode, seatNo
            from TravelEmptySeatUView as ES
            where ES.travelCode = "''' + travel_code + '''";
        '''


def query_paymet_status(order_no, travel_code):
    return '''
            select paymentStatus 
            from ORDER
            where travelCode = "''' + travel_code + '''"
            and orderNo = "''' + order_no + '''"
        ;'''


def query_discount_percents(order_no, travel_code):
    return '''
                select percent
                from DISCOUNT
                where travelCode = "''' + travel_code + '''"
                and orderNo = "''' + order_no + '''"
            ;'''
