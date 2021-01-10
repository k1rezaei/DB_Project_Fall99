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
                             , '[5] Customers list based on number of travels'
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
            self.manager_customer_list_by_travels()
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
        print("----------\nPress Y to go back!")
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
        Terminal.fancy_print('Enter user\'s NC', 'Discount No',
                             'Discount Percent', 'Expiration time (YYYY-MM-DD HH:MM:SS)')

        nc = input()
        discount_no = input()
        percent = int(input())
        expiration_time = input()
        try:
            self.execute_database_query(
                ManagerQueries.get_add_discount_query(nc, discount_no,
                                                      percent, expiration_time))
            print('Giving discount successful')
        except (Exception, Error) as error:
            print("Error while inserting discount", error)

        self.manager_back_to_main()

    def manager_target_city_list(self):
        try:
            cities = self.execute_database_query(
                ManagerQueries.get_target_city_query())

            print(cities) # TODO print?
        except (Exception, Error) as error:
            print("Error while fetching target city data", error)

        self.manager_back_to_main()

    def manager_airplane_list_in_city(self):
        Terminal.fancy_print("Enter city name:")
        city = input()
        try:
            airplanes = self.execute_database_query(
                ManagerQueries.get_airplanes_in_city_query(city))
            print(airplanes) # TODO print?
        except (Exception, Error) as error:
            print("Error while fetching airplanes", error)

        self.manager_back_to_main()

    def manager_score_employees(self):
        try:
            employees = self.execute_database_query(
                ManagerQueries.get_employee_score_query())
            print(employees) # TODO print?
        except (Exception, Error) as error:
            print("Error while fetching employees\' scores", error)

        self.manager_back_to_main()

    def manger_score_airplanes(self):
        try:
            airplanes = self.execute_database_query(
                ManagerQueries.get_airplane_score_query())
            print(airplanes) # TODO print?
        except (Exception, Error) as error:
            print("Error while fetching airplanes\' scores", error)

        self.manager_back_to_main()

    def manager_score_captains(self):
        try:
            captains = self.execute_database_query(
                ManagerQueries.get_captains_score_query())
            print(captains) # TODO print?
        except (Exception, Error) as error:
            print("Error while fetching captains\' scores", error)

        self.manager_back_to_main()

    def manager_scores(self):
        Terminal.fancy_print('[1] See employees\' scores',
                             '[2] See airplanes\' scores',
                             '[3] See captains\' scores')
        query = input()
        if query == '1':
            self.manager_score_employees()
        elif query == '2':
            self.manger_score_airplanes()
        else:
            self.manager_score_captains()

    def manager_customer_list_by_travels(self):
        try:
            all_customers = self.execute_database_query(
                ManagerQueries.get_customers_by_travels())

            print(all_customers) # TODO print?
        except (Exception, Error) as error:
            print("Error while fetching customers\' travels", error)

        self.manager_back_to_main()

    def manager_customer_list(self):
        try:
            all_customers = self.execute_database_query(
                ManagerQueries.get_all_customers_query())

            print(all_customers) # TODO print?
        except (Exception, Error) as error:
            print("Error while fetching customers", error)

        self.manager_back_to_main()

    def manager_airplane_list(self):
        try:
            all_airplanes = self.execute_database_query(
                ManagerQueries.get_all_airplanes_query())

            print(all_airplanes) # TODO print?
        except (Exception, Error) as error:
            print("Error while fetching airplanes", error)

        self.manager_back_to_main()

    def manager_employee_list(self):
        try:
            all_employees = self.execute_database_query(
                ManagerQueries.get_all_employees_query())

            print(all_employees) # TODO print?
        except (Exception, Error) as error:
            print("Error while fetching employees", error)

        self.manager_back_to_main()

    def manager_travel_list(self):
        try:
            all_travels = self.execute_database_query(
                ManagerQueries.get_all_travels_query())

            print(all_travels) # TODO print?
        except (Exception, Error) as error:
            print("Error while fetching travels", error)

        self.manager_back_to_main()

    def manager_entity_lists(self):
        Terminal.fancy_print('[1] See customers',
                             '[2] See airplanes',
                             '[3] See employees',
                             '[4] See travels')
        query = input()
        if query == '1':
            self.manager_customer_list()
        elif query == '2':
            self.manager_airplane_list()
        elif query == '3':
            self.manager_employee_list()
        else:
            self.manager_travel_list()

    def manager_give_salaries(self):
        try:
            self.execute_database_query(
                ManagerQueries.get_give_salary_query())
            print("Giving salaries successful")
        except (Exception, Error) as error:
            print("Error while giving salaries", error)

        self.manager_back_to_main()


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
