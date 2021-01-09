import psycopg2
from psycopg2 import Error
from Login import my_database, my_password


def execute_data_base_query(cursor, query):
    try:
        cursor.execute(query)
    except (Exception, Error) as error:
        print(error)


class Terminal:
    def __init__(self, cursor):
        self.cursor = cursor
        self.current_username = None
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
        Terminal.fancy_print("Welcome!", "Choose one of theese options to continue:"
                             , "[1] Register"
                             , "[2] Login")
        query = int(input())
        if query == 1:
            self.register()
        else:
            self.login()

    def register(self):
        Terminal.fancy_print('Enter enter your username:')
        username = input()
        Terminal.fancy_print('Enter your password:')
        password = input()
        self.execute_database_query('insert into ACCOUNT VALUES (' + username + ', ' + password + ', False);')
        self.current_username = username
        Terminal.fancy_print('Your registration completed!', 'Thanks for choosing us!')

    def login(self):
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
