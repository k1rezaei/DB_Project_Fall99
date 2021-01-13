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
            self.user_discounts()
        elif query == 2:
            self.user_budget()
        elif query == 3:
            self.user_all_flights()
        elif query == 4:
            self.user_personal_flights()
        elif query == 5:
            self.user_buy_ticket()
        elif query == 6:
            self.user_comment()
        else:
            self.current_username = None
            self.current_NC = None
            self.is_manager = False
            self.start()

    def user_discounts(self):
        answer = self.execute_database_query('''
            select discountNo, percent, expirationTime
            from DISCOUNT as D
            where D.customerNc == ''' + self.current_NC + '''
            and D.orderNo is null
            and clock_timestamp() > D.expirationTime;
            ''')
        if len(answer) == 0:
            Terminal.fancy_print('Nothing to display!')
        else:
            print(answer)  # TODO khoshgel kardane khorooji

        self.user_main()

    def user_budget(self):
        answer = self.execute_database_query('''
            select money
            from CUSTOMER as C
            where C.customerNc == "''' + self.current_NC + '''"
            ;''')
        money = answer[0][0]
        Terminal.fancy_print("Your wallet: " + str(money) + "$", "Choose one of theese options:"
                             , "[1] Add money to your wallet (don't worry in this version, it's completely free"
                             , "    but PLEASE don't overuse this option)"
                             , "[2] Back to main menu")
        query = int(input())
        if query == 1:
            Terminal.fancy_print("Amount of money you want to pay:")
            amount_of_money = int(input())
            new_money = money + amount_of_money
            self.execute_database_query('''
                update CUSTOMER
                set money=''' + str(new_money) + '''
                from CUSTOMER as C
                where C.customerNc == ''' + self.current_NC + '''
                ;''')
            self.user_budget()
        else:
            self.user_main()

    def user_all_flights(self):
        answer = self.execute_database_query('''
            select *
            from TRAVEL as T
            where clock_timestamp() < T.time;
            ''')
        if len(answer) == 0:
            Terminal.fancy_print('Nothing to display!')
        else:
            print(answer)  # TODO khoshgel kardane khorooji

        self.user_main()

    def user_personal_past_flights(self):
        answer = self.execute_database_query('''
            select T.code, T.time, T.startingCity, T.targetCity, 
                    T.ticketPrice, T.airplaneCode, O.seatNo ,O.paymentStatus
            from TRAVEL as T, ORDER as O
            where clock_timestamp() >= T.time
            and O.travelCode = T.code
            and O.customerNC = "''' + self.current_NC + '''"
            ;''')
        if len(answer) == 0:
            Terminal.fancy_print('Nothing to display!')
        else:
            print(answer)  # TODO khoshgel kardane khorooji

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
                select T.code, T.time, T.startingCity, T.targetCity, 
                        T.ticketPrice, T.airplaneCode, O.seatNo ,O.paymentStatus
                from TRAVEL as T, ORDER as O
                where clock_timestamp() < T.time
                and O.travelCode = T.code
                and O.customerNC = "''' + self.current_NC + '''"
                ;''')
        if len(answer) == 0:
            Terminal.fancy_print('Nothing to display!')
        else:
            print(answer)  # TODO khoshgel kardane khorooji

        Terminal.fancy_print("Choose one of theese options:",
                             "[1] Cancel a travel",
                             "[2] Back to main menu")
        query = int(input())
        if query == 1:
            Terminal.fancy_print("Travel cancelation", "Enter travel code:")
            # TODO sakhte injash :))
            self.user_personal_future_flights()
        else:
            self.user_main()

    def user_buy_ticket(self):
        Terminal.fancy_print("Enter travel code:")
        travel_code = input()
        # TODO

    def user_comment(self):
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
            , "''' + query_comment + '''")
        ''')

    def user_personal_flights(self):
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
