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
