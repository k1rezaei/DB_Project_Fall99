from psycopg2._psycopg import Error


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
