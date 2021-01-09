import psycopg2
from psycopg2 import Error
from Login import my_database, my_password


def execute_data_base_query(cursor, query):
    cursor.execute(query)


class Terminal:
    def __init__(self, cursor):
        self.cursor = cursor
        self.current_username = ""
        self.is_manager = False

    def execute_database_query(self, query):
        execute_data_base_query(self.cursor, query)

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
                             , "[1] Offers!"
                             , "[2] Budget"
                             , "[3] Flights"
                             , "[4] Your flights"
                             , "[5] Buy ticket"
                             , "[6] Contact to manager")
        query = int(input())
        if query == 1:
            self.user_offers()
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

    def user_offers(self):
        pass

    def user_budget(self):
        pass

    def user_all_flights(self):
        pass

    def user_personal_flights(self):
        pass

    def user_buy_ticket(self):
        pass

    def user_comment(self):
        pass

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
        pass

    def manager_add_remove_airplane(self):
        pass

    def manager_user_comments(self):
        pass

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
