from psycopg2._psycopg import Error


def change(query: str):
    return query.replace('"', '\'')


def get_first(query: str):
    for c in query:
        if c == '\n' or c == ' ':
            continue
        return c


def execute_data_base_query(cursor, connection, query):
    new_query = change(query)
    cursor.execute(change(query))
    result = []
    if get_first(new_query) == 's' or get_first(new_query) == 'S':
        result = cursor.fetchall()
    connection.commit()
    return result


class Terminal:
    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection
        self.current_NC = None  # it must be a string

    def execute_database_query(self, query):
        return execute_data_base_query(self.cursor, self.connection, query)

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

    @staticmethod
    def table_print(table, header):
        out = ""
        for x in header:
            out += str(x) + "\t"
        print(out)

        for row in table:
            out = ""
            for item in row:
                out += str(item) + "\t"
            print(out)
