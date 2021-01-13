from Terminal.Terminal import Terminal
from psycopg2._psycopg import Error

from Queries.UserQueries import query_discount_set_null, query_all_future_flights, query_travel_price, \
    query_empty_seats, query_paymet_status, query_discount_percents


class UserTerminal(Terminal):

    def start(self):
        Terminal.fancy_print("Welcome!", "Choose one of theese options:"
                             , "[1] Register"
                             , "[2] Login"
                             , "[3] Exit")
        query = int(input())
        if query == 1:
            self.register()
        elif query == 2:
            self.login()
        else:
            Terminal.fancy_print("Goodbye!")
            return

    def register(self):
        Terminal.fancy_print('Enter enter your National Code:')
        nc = input()
        Terminal.fancy_print('Enter your password:')
        password = input()
        Terminal.fancy_print('Enter your first name')
        first_name = input()
        Terminal.fancy_print('Enter your lastname')
        last_name = input()
        try:
            self.execute_database_query('insert into CUSTOMER VALUES ("' + nc + '", "' + password +
                                        '", "' + first_name + '", "' + last_name + '", 0);')
        except (Exception, Error) as error:
            print(error)
            Terminal.fancy_print("Your registration failed!")
            self.start()
            return
        self.current_NC = nc
        Terminal.fancy_print('Your registration completed!', 'Thanks for choosing us!')
        self.user_main()

    def login(self):
        Terminal.fancy_print('Enter enter your National Code:')
        nc = input()
        Terminal.fancy_print('Enter your password:')
        password = input()
        query = 'SELECT * FROM CUSTOMER WHERE NC = "' + nc + '" and password = "' + password + '";'
        is_registered = self.execute_database_query(query)
        if len(is_registered) > 0:
            self.current_NC = nc
            self.user_main()
        else:
            Terminal.fancy_print('You are Not Registered!')
            self.register()

    def user_main(self):
        Terminal.fancy_print("User: " + self.current_NC + "!",
                             "Choose one of theese options:",
                             "[1] Your discounts",
                             "[2] Budget",
                             "[3] Flights",
                             "[4] Your flights",
                             "[5] Buy ticket",
                             "[6] Contact to manager",
                             "[7] logout")
        query = int(input())
        if query == 1:
            self.discounts()
            self.user_main()
        elif query == 2:
            self.budget()
            self.user_main()
        elif query == 3:
            self.all_flights()
            self.user_main()
        elif query == 4:
            self.personal_flights()
            self.user_main()
        elif query == 5:
            self.buy_ticket()
            self.user_main()
        elif query == 6:
            self.comment()
            self.user_main()
        else:
            self.current_NC = None
            self.start()

    def discounts(self):
        answer = []
        try:
            answer = self.execute_database_query(self.query_not_expired_discounts())
        except (Exception, Error) as error:
            print(error)

        if len(answer) == 0:
            Terminal.fancy_print('No discount to display!')
            return False
        else:
            Terminal.table_print(answer, ["discountNo", "percent", "expirationTime"])
            return True

    def budget(self):
        money = self.get_money()
        Terminal.fancy_print("Your wallet: " + str(money) + "$", "Choose one of theese options:",
                             "[1] Add money to your wallet (don't worry in this version, it's completely free",
                             "    but PLEASE don't overuse this option)",
                             "[2] Back to main menu")
        query = int(input())
        if query == 1:
            Terminal.fancy_print("Amount of money you want to pay:")
            amount_of_money = int(input())
            self.change_money(amount_of_money)
            self.budget()

    def change_money(self, toadd_money):
        money = self.get_money()
        new_money = money + toadd_money

        try:
            self.execute_database_query(self.query_change_money(new_money))

            return True
        except (Exception, Error) as error:
            print(error)
            return False

    def get_money(self):
        answer = self.execute_database_query(self.query_get_money())
        money = answer[0][0]
        return money

    def all_flights(self):
        database_query = query_all_future_flights()

        Terminal.fancy_print("Choose one of theese options:",
                             "[1] Order by number of empty seats",
                             "[2] Order by airplane score",
                             "[3] Order by ticket price")
        query = int(input())
        if query == 1:
            database_query += "order by emptySeats;"
        elif query == 2:
            database_query += "order by AirS.avgScore;"
        elif query == 3:
            database_query += "order by T.ticketPrice;"

        answer = []
        try:
            answer = self.execute_database_query(database_query)
        except (Exception, Error) as error:
            print(error)

        if len(answer) == 0:
            Terminal.fancy_print('Nothing to display!')
        else:
            Terminal.table_print(answer, ["code", "time", "startCity", "targetCity", "ticketPrice",
                                          "airplaneCode", "captainCode", "avgScore", "emptySeats"])

    def user_personal_past_flights(self):
        answer = self.execute_database_query(self.query_personal_past_flights())
        if len(answer) == 0:
            Terminal.fancy_print('Nothing to display!')
        else:
            Terminal.table_print(answer, ["travelCode", "orderNo", "time", "startingCity", "targetCity",
                                          "ticketPrice", "airplaneCode", "seatNo", "paymentStatus"])

        Terminal.fancy_print("Choose one of theese options:",
                             "[1] Score a travel",
                             "[2] Back to main menu")
        query = int(input())
        if query == 1:
            Terminal.fancy_print("Travel Scoring", "Enter order number:")
            order_no = input()
            Terminal.fancy_print("Order " + str(order_no), "Enter your score:")
            score = float(input())
            try:
                self.execute_database_query(self.query_score_flight(order_no, score))
            except (Exception, Error) as error:
                print(error)
                Terminal.fancy_print("Your scoring failed!")

            self.user_personal_past_flights()

    def user_personal_future_flights(self):
        answer = self.execute_database_query(self.query_future_flights())

        if len(answer) == 0:
            Terminal.fancy_print('Nothing to display!')
        else:
            Terminal.table_print(answer, ["travelCode", "orderNo", "time", "startingCity", "targetCity",
                                          "ticketPrice", "airplaneCode", "seatNo", "paymentStatus"])

        Terminal.fancy_print("Choose one of theese options:",
                             "[1] Cancel an order",
                             "[2] Back to main menu")
        query = int(input())
        if query == 1:
            Terminal.fancy_print("Travel cancelation", "Enter travel code:")
            travel_code = input()

            Terminal.fancy_print("Enter order number")
            order_no = input()

            payment_status = self.execute_database_query(query_paymet_status(order_no, travel_code))[0][0]
            if payment_status == 'Paid':
                price = self.get_travel_price(travel_code)

                discounts = self.execute_database_query(
                    query_discount_percents(order_no, travel_code))

                price *= self.get_percent_discount(discounts)

                self.execute_database_query(query_discount_set_null(order_no, travel_code))
                self.execute_database_query(self.query_set_order_status(order_no, 'NotPaid'))

                self.change_money(price * 0.95)
                self.fancy_print("95% of your payment back to your wallet")
            else:
                self.fancy_print("This order is not paid!")

            self.user_personal_future_flights()

    def buy_ticket(self):
        Terminal.fancy_print("Enter travel code:")
        travel_code = input()
        answer = self.execute_database_query(query_empty_seats(travel_code))

        if len(answer) == 0:
            Terminal.fancy_print('Nothing to display!')
            return
        else:
            Terminal.table_print(answer, ['airplaneCode', 'seatNo'])

            Terminal.fancy_print("Enter airplane code:")
            airplane_code = input()

            Terminal.fancy_print("Enter seat no:")
            seat_no = input()

            Terminal.fancy_print("Enter order no:")
            order_no = input()

            self.execute_database_query(self.query_insert_order(airplane_code, order_no, seat_no, travel_code))
            discounts = []
            if self.discounts():
                Terminal.fancy_print("Do you want to use your discounts",
                                     "for this order?",
                                     "[1] Yes",
                                     "[2] No")
                query = int(input())

                price = self.get_travel_price(travel_code)

                if query == 1:
                    Terminal.fancy_print("Enter discount numbers (e.g. 23 34 12)")
                    discounts = input().split(" ")
                    flag = True
                    for discount_no in discounts:
                        flag = flag and self.execute_database_query(self.query_is_available_discount(discount_no))[0][0]

                    if flag:
                        price *= self.get_percent_discount(discounts)

            if self.get_money() < price:
                self.fancy_print("Price: " + str(price) + "$",
                                 "You have not enough money to buy ticket!")
            else:
                self.change_money(-price)

                for discount_no in discounts:
                    self.execute_database_query(self.query_use_discount(discount_no, order_no))

                self.execute_database_query(self.query_set_order_status(order_no, 'Paid'))
                self.fancy_print("You bought the ticket!",
                                 "Price: " + str(price) + "$")

    def get_percent_discount(self, discounts):
        mult_discounts = 1.0
        for discount_no in discounts:
            mult_discounts *= self.execute_database_query(self.query_percent_single_discount(discount_no))[0][0] / 100.0
        return mult_discounts

    def get_travel_price(self, travel_code):
        return self.execute_database_query(query_travel_price(travel_code))[0][0]

    def comment(self):
        Terminal.fancy_print("Enter your comment number:")
        comment_number = input()
        Terminal.fancy_print("Write your comment:",
                             "End your comment with a line with only a dot")
        comment = [input()]
        while comment[-1] != '.':
            comment.append(input())

        comment = comment[:-1]
        # TODO in doroste too postgresql? injori enter mizanan?
        query_comment = ''
        for c in comment:
            query_comment += c
            query_comment += '\\n'

        self.execute_database_query(self.query_insert_comment(comment_number, query_comment))

    def personal_flights(self):
        Terminal.fancy_print("Choose one of these options:",
                             '[1] Past flights',
                             '[2] Future flights',
                             '[3] Back to main menu'
                             )
        query = int(input())
        if query == 1:
            self.user_personal_past_flights()
        elif query == 2:
            self.user_personal_future_flights()

    def query_not_expired_discounts(self):
        return '''
                select discountNo, percent, expirationTime
                from DISCOUNT as D
                where D.customerNc = "''' + self.current_NC + '''"
                and D.orderNo is null
                and clock_timestamp() > D.expirationTime;
                '''

    def query_change_money(self, new_money):
        return '''
                    update CUSTOMER
                    set money=''' + str(new_money) + '''
                    where CUSTOMER.NC = "''' + self.current_NC + '''";'''

    def query_is_available_discount(self, discount_no):
        return '''
                    select (expirationTime > clock_timestamp() and orderNo is null)
                    from DISCOUNT
                    where discountNo = "''' + discount_no + '''"
                    and customerNC = "''' + self.current_NC + '''"
                '''

    def query_get_money(self):
        return '''
                    select money
                    from CUSTOMER as C
                    where C.NC = "''' + self.current_NC + '''"
                    ;'''

    def query_score_flight(self, order_no, score):
        return '''
                    update ORDER_TABLE
                    set score=''' + str(score) + '''
                    where customerNC = "''' + self.current_NC + '''"
                    and orderNo = "''' + order_no + '''";
                '''

    def query_personal_past_flights(self):
        return '''
            select T.code, O.orderNo, T.time, T.startCity, T.targetCity, 
                    T.ticketPrice, T.airplaneCode, O.seatNo ,O.paymentStatus
            from TRAVEL as T, ORDER_TABLE as O
            where clock_timestamp() >= T.time
            and O.travelCode = T.code
            and O.customerNC = "''' + self.current_NC + '''"
            ;'''

    def query_set_order_status(self, order_no, new_status):
        return '''
                    update ORDER_TABLE
                    set paymentStatus = "''' + new_status + '''"
                    where customerNC = "''' + self.current_NC + '''"
                    and orderNo = "''' + order_no + '''"
                ;'''

    def query_future_flights(self):
        return '''
                select T.code, O.orderNo, T.time, T.startCity, T.targetCity, 
                        T.ticketPrice, T.airplaneCode, O.seatNo ,O.paymentStatus
                from TRAVEL as T, ORDER_TABLE as O
                where clock_timestamp() < T.time
                and O.travelCode = T.code
                and O.customerNC = "''' + self.current_NC + '''"
                ;'''

    def query_insert_order(self, airplane_code, order_no, seat_no, travel_code):
        return '''
                insert into ORDER_TABLE
                values ("''' + self.current_NC + '''", "''' + order_no + '''",
                    'NotPaid', "''' + travel_code + '''", null, "''' + seat_no + '''",
                    "''' + airplane_code + '''");   
            '''

    def query_percent_single_discount(self, discount_no):
        return '''
                    select percent 
                    from DISOUNT 
                    where D.customerNC = "''' + self.current_NC + '''"
                    and D.discountNo = "''' + discount_no + '''"
                    ;
                '''

    def query_use_discount(self, discount_no, order_no):
        return '''
                    update DISCOUNT as D
                    set D.customerOrderNC = "''' + self.current_NC + '''",
                        D.Order_No = "''' + order_no + '''"
                    where D.customerNC = "''' + self.current_NC + '''"
                    and D.discountNo = "''' + discount_no + '''"
                    ;
                '''

    def query_set_discount_to_null(self):
        return '''
                    update DISCOUNT as D
                    set D.customerOrderNC = null,
                        D.Order_No = null
                    where D.customerNC = "''' + self.current_NC + '''"
                    ;
                '''

    def query_insert_comment(self, comment_number, query_comment):
        return '''
            insert into COMMENT values ("''' + self.current_NC + '''",
            "''' + comment_number + '''",
            "''' + query_comment + '''");
        '''
