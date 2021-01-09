import psycopg2
from psycopg2 import Error
from Login import my_database, my_password
import ManagerQueries


def execute_data_base_query(cursor, query):
    return cursor.fetchall()


class Terminal:
    def __init__(self, cursor):
        self.cursor = cursor
        self.current_username = ""
        self.current_NC = None  # it must be a string
        self.is_manager = False

    def execute_database_query(self, query):
        return execute_data_base_query(self.cursor, query)

    @staticmethod
    def fancy_print(*strings):
        border = '~'
        maxi = 0
        for s in strings:
            maxi = max(maxi, len(s))

        print(border * (maxi + 6))
        for s in strings:
            print(border * 2 + " " + s + " " * (maxi - len(s) + 1) + border * 2)
        print(border * (maxi + 6))

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
        Terminal.fancy_print('Enter enter your username:')
        username = input()
        Terminal.fancy_print('Enter your password:')
        password = input()
        try:
            self.execute_database_query('insert into ACCOUNT VALUES (' + username + ', ' + password + ', False);')
        except (Exception, Error) as error:
            print(error)
            Terminal.fancy_print("Your registration failed!")
            self.start()
            return
        self.current_username = username
        Terminal.fancy_print('Your registration completed!', 'Thanks for choosing us!')
        self.user_main()

    def login(self):
        pass

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

    def manager_main(self):
        Terminal.fancy_print("Welcome back " + self.current_username + "!", "Choose one of these options:"
                             , '[1] Add new flight'
                             , '[2] Add/Remove airplane'
                             , '[3] User\'s comments'
                             , '[4] Giving discount to users'
                             , '[5] Customers list'
                             , '[6] Target city list'
                             , '[7] Airplanes list in a city'
                             , '[8] Analyzing scores'
                             , '[9] See entity lists'
                             , '[10] Give salary to employees'
                             )
        query = int(input())
        if query == 1:
            self.manager_add_flight()
        elif query == 2:
            self.manager_add_remove_airplane()
        elif query == 3:
            self.manager_user_comments()
        elif query == 4:
            self.manager_give_discount()
        elif query == 5:
            self.manager_customer_list()
        elif query == 6:
            self.manager_target_city_list()
        elif query == 7:
            self.manager_airplane_list_in_city()
        elif query == 8:
            self.manager_scores()
        elif query == 9:
            self.manager_entity_lists()
        elif query == 10:
            self.manager_give_salaries()

    def manager_add_flight(self):
        all_flights = self.execute_database_query(ManagerQueries.get_all_flight_query())
        new_code = len(all_flights)
        Terminal.fancy_print('Enter Following Information:',
                             'Time (YYYY-MM-DD HH:MM:SS)',
                             'Starting city',
                             'Target city',
                             'Ticket price',
                             'Airplane code',
                             'Captain code')
        time = input()
        starting_city = input()
        target_city = input()
        ticket_price = int(input())
        airplane_code = int(input())
        captain_code = int(input())

        try:
            self.execute_database_query(ManagerQueries.get_add_flight_query(new_code, time, starting_city, target_city,
                                                                            ticket_price, airplane_code, captain_code))
            print("Flight added successfully!")
        except (Exception, Error) as error:
            print("Error while inserting new flight", error)

        self.manager_back_to_main()

    def manager_back_to_main(self):
        print("Press Y to go back!")
        tmp = input()
        self.manager_main()

    def manager_add_airplane(self):
        all_airplanes = self.execute_database_query(ManagerQueries.get_all_airplanes_query())
        new_code = len(all_airplanes)
        Terminal.fancy_print('Enter following information:',
                             'Capacity', 'Model', 'CIty')
        cap = int(input())
        model = input()
        city = input()
        try:
            self.execute_database_query(
                ManagerQueries.get_add_airplane_query(new_code, cap, model, city))
            print("Airplane added successfully!")
        except (Exception, Error) as error:
            print("Error while inserting new airplane", error)

        self.manager_back_to_main()

    def manager_remove_airplane(self):
        Terminal.fancy_print('Enter airplane\'s code')
        code = int(input())
        try:
            self.execute_database_query(
                ManagerQueries.get_remove_airplane_query(code))
            print("Airplane removed successfully!")
        except (Exception, Error) as error:
            print("Error while removing airplane", error)

        self.manager_back_to_main()

    def manager_add_remove_airplane(self):
        Terminal.fancy_print("[1] Add an airplane", '[2] Remove airplane')
        query = int(input())
        if query == 1:
            self.manager_add_airplane()
        else:
            self.manager_remove_airplane()

    def manager_user_comments(self):
        try:
            all_comments = self.execute_database_query(
                ManagerQueries.get_all_comments_query())
            print(all_comments)
        except (Exception, Error) as error:
            print("Error while fetching comments", error)

        self.manager_back_to_main()

    def manager_give_discount(self):
        pass

    def manager_customer_list(self):
        pass

    def manager_target_city_list(self):
        pass

    def manager_airplane_list_in_city(self):
        pass

    def manager_scores(self):
        pass

    def manager_entity_lists(self):
        pass

    def manager_give_salaries(self):
        pass


if __name__ == '__main__':
    try:
        connection = psycopg2.connect(user="postgres",
                                      password=my_password,
                                      host="127.0.0.1",
                                      database=my_database)
        cursor = connection.cursor()

        terminal = Terminal(cursor)
        terminal.start()

        '''# Print PostgreSQL details
        print("PostgreSQL server information")
        print(connection.get_dsn_parameters(), "\n")
        cursor.execute("SELECT version();")
        # Fetch result
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")'''

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
