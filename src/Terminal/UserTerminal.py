from Terminal.Terminal import Terminal


class UserTerminal(Terminal):
    def user_main(self):
        Terminal.fancy_print("Welcome back " + self.current_username + "!", "Choose one of theese options:"
                             , "[1] Your discounts"
                             , "[2] Budget"
                             , "[3] Flights"
                             , "[4] Your flights"
                             , "[5] Buy ticket"
                             , "[6] Contact to manager"
                             , "[7] logout")
        query = int(input())
        if query == 1:
            self.discounts()
        elif query == 2:
            self.budget()
        elif query == 3:
            self.all_flights()
        elif query == 4:
            self.personal_flights()
        elif query == 5:
            self.buy_ticket()
        elif query == 6:
            self.comment()
        else:
            self.current_username = None
            self.current_NC = None
            self.is_manager = False
            self.start()

    def discounts2(self):
        answer = self.execute_database_query('''
            select discountNo, percent, expirationTime
            from DISCOUNT as D
            where D.customerNc == ''' + self.current_NC + '''
            and D.orderNo is null
            and clock_timestamp() > D.expirationTime;
            ''')
        if len(answer) == 0:
            Terminal.fancy_print('No discount to display!')
            return False
        else:
            Terminal.table_print(answer, ["discountNo", "percent", "expirationTime"])
            return True

    def discounts(self):
        self.discounts2()
        self.user_main()

    def budget(self):
        money = self.get_money()
        Terminal.fancy_print("Your wallet: " + str(money) + "$", "Choose one of theese options:"
                             , "[1] Add money to your wallet (don't worry in this version, it's completely free"
                             , "    but PLEASE don't overuse this option)"
                             , "[2] Back to main menu")
        query = int(input())
        if query == 1:
            Terminal.fancy_print("Amount of money you want to pay:")
            amount_of_money = int(input())
            self.change_money(amount_of_money)
            self.budget()
        else:
            self.user_main()

    def change_money(self, toadd_money):
        money = self.get_money()
        new_money = money + toadd_money
        self.execute_database_query('''
                update CUSTOMER
                set money=''' + str(new_money) + '''
                from CUSTOMER as C
                where C.customerNc == ''' + self.current_NC + '''
                ;''')

    def get_money(self):
        answer = self.execute_database_query('''
                    select money
                    from CUSTOMER as C
                    where C.customerNc == "''' + self.current_NC + '''"
                    ;''')
        money = answer[0][0]
        return money

    def all_flights(self):
        database_query = '''
                    select *, (select count(*)
                                from TravelEmptySeatUView as ES 
                                where T.code=ES.travelCode
                    ) as emptySeats
                    from TRAVEL as T, AirplaneScoreUView as AirS
                    where clock_timestamp() < T.time
                    and T.airplaneCode = AirS.airplaneCode
                    '''

        Terminal.fancy_print("Choose one of theese options:",
                             "[1] Order by number of empty seats",
                             "[2] Order by airplane score",
                             "[3] Order by ticket price")
        query = int(input())
        if query == 1:
            database_query += "order by emptySeats"
        elif query == 2:
            database_query += "order by AirS.avgScore"
        elif query == 3:
            database_query += "order by T.price"

        answer = self.execute_database_query(database_query)

        if len(answer) == 0:
            Terminal.fancy_print('Nothing to display!')
        else:
            Terminal.table_print(answer, ["code", "time", "startCity", "targetCity", "ticketPrice",
                                          "airplaneCode", "captainCode", "avgScore", "emptySeats"])

        self.user_main()

    def user_personal_past_flights(self):
        answer = self.execute_database_query('''
            select T.code, O.orderNo, T.time, T.startingCity, T.targetCity, 
                    T.ticketPrice, T.airplaneCode, O.seatNo ,O.paymentStatus
            from TRAVEL as T, ORDER as O
            where clock_timestamp() >= T.time
            and O.travelCode = T.code
            and O.customerNC = "''' + self.current_NC + '''"
            ;''')
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
            self.execute_database_query('''
                update ORDER
                set score=''' + str(score) + '''
                where customerNC ="''' + self.current_NC + '''"
                and orderNo="''' + order_no + '''";
            ''')
            self.user_personal_past_flights()
        else:
            self.user_main()

    def user_personal_future_flights(self):
        answer = self.execute_database_query('''
                select T.code, O.orderNo, T.time, T.startingCity, T.targetCity, 
                        T.ticketPrice, T.airplaneCode, O.seatNo ,O.paymentStatus
                from TRAVEL as T, ORDER as O
                where clock_timestamp() < T.time
                and O.travelCode = T.code
                and O.customerNC = "''' + self.current_NC + '''"
                ;''')
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

            paymentStatus = self.execute_database_query('''
                select paymentStatus 
                from ORDER
                where travelCode = "''' + travel_code + '''"
                and orderNo = "''' + order_no + '''"
                ;
            ''')[0][0]
            if paymentStatus == 'Paid':
                price = self.get_travel_price(travel_code)

                discounts = self.execute_database_query('''
                    select percent
                    from DISCOUNT
                    where travelCode = "''' + travel_code + '''"
                    and orderNo = "''' + order_no + '''"
                    ;
                ''')

                price *= self.get_percent_discount(discounts)

                self.execute_database_query('''
                    update DISCOUNT 
                    set orderNo = null, customerOrderNC = null
                    where travelCode = "''' + travel_code + '''"
                    and orderNo = "''' + order_no + '''"
                    ;
                ''')

                self.change_money(price * 0.95)
                self.fancy_print("95% of your payment back to your wallet")
            else:
                self.fancy_print("This order is not paid!")

            self.user_personal_future_flights()
        else:
            self.user_main()

    def buy_ticket(self):
        Terminal.fancy_print("Enter travel code:")
        travel_code = input()
        answer = self.execute_database_query('''
            select airplaneCode, seatNo
            from TravelEmptySeatUView as ES
            where ES.travelCode = "''' + travel_code + '''";
        ''')

        if len(answer) == 0:
            Terminal.fancy_print('Nothing to display!')
            self.user_main()
        else:
            Terminal.table_print(answer, ['airplaneCode', 'seatNo'])

            Terminal.fancy_print("Enter airplane code:")
            airplane_code = input()

            Terminal.fancy_print("Enter seat no:")
            seat_no = input()

            Terminal.fancy_print("Enter order no:")
            order_no = input()

            self.execute_database_query('''
                insert into order
                values ("''' + self.current_NC + '''", "''' + order_no + '''",
                    'NotPaid', "''' + travel_code + '''", null, "''' + seat_no + '''",
                    "''' + airplane_code + '''");   
            ''')
            if self.discounts2():
                Terminal.fancy_print("Do you want to use your discounts",
                                     "for this order?",
                                     "[1] Yes",
                                     "[2] No")
                query = int(input())

                price = self.get_travel_price(travel_code)

                if query == 1:
                    Terminal.fancy_print("Enter discount numbers (e.g. 23 34 12)")
                    discounts = input().split(" ")
                    self.execute_database_query('''
                        update DISCOUNT as D
                        set D.customerOrderNC = null
                            , D.Order_No = null
                        where D.customerNC = "''' + self.current_NC + '''"
                        ;
                    ''')
                    price *= self.get_percent_discount(discounts)

                    for discount_no in discounts:
                        self.execute_database_query('''
                            update DISCOUNT as D
                            set D.customerOrderNC = "''' + self.current_NC + '''"
                                , D.Order_No = "''' + order_no + '''"
                            where D.customerNC = "''' + self.current_NC + '''"
                            and D.discountNo = "''' + discount_no + '''"
                            ;
                        ''')

                if self.get_money() < price:
                    self.fancy_print("Price: " + str(price) + "$",
                                     "You have not enough money to buy ticket!")
                else:
                    self.change_money(-price)
                    self.execute_database_query('''
                        update ORDER
                        set paymentStatus = 'Paid'
                        where customerNC = "''' + self.current_NC + '''"
                        and orderNo = "''' + order_no + '''";
                    ''')
                    self.fancy_print("You bought the ticket!",
                                     "Price: " + str(price) + "$")

    def get_percent_discount(self, discounts):
        mult_discounts = 1.0
        for discount_no in discounts:
            mult_discounts *= self.execute_database_query('''
                            select percent 
                            from DISOUNT 
                            where D.customerNC = "''' + self.current_NC + '''"
                            and D.discountNo = "''' + discount_no + '''"
                            ;
                        ''')[0][0] / 100.0
        return mult_discounts

    def get_travel_price(self, travel_code):
        return self.execute_database_query('''
                    select price 
                    from TRAVEL 
                    where code = "''' + travel_code + '''"
                ''')[0][0]

    def comment(self):
        Terminal.fancy_print("Enter your comment number:")
        comment_number = input()
        Terminal.fancy_print("Write your comment:"
                             , "End your comment with a line with only a dot")
        comment = [input()]
        while comment[-1] != '.':
            comment.append(input())

        comment = comment[:-1]
        # TODO in doroste too postgresql? injori enter mizanan?
        query_comment = ''
        for c in comment:
            query_comment += c
            query_comment += '\\n'

        self.execute_database_query('''
            insert into COMMENT values ("''' + self.current_NC + '''"
            , "''' + comment_number + '''"
            , "''' + query_comment + '''");
        ''')

    def personal_flights(self):
        Terminal.fancy_print("Choose one of these options:"
                             , '[1] Past flights'
                             , '[2] Future flights'
                             , '[3] Back to main menu'
                             )
        query = int(input())
        if query == 1:
            self.user_personal_past_flights()
        elif query == 2:
            self.user_personal_future_flights()
        else:
            self.user_main()
