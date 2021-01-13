from psycopg2._psycopg import Error


def change(query: str):
    return query.replace('"', '\'')


def execute_data_base_query(cursor, query):
    print(query)
    print(change(query))
    cursor.execute(change(query))
    return cursor.fetchall()


class Terminal:
    def __init__(self, cursor):
        self.cursor = cursor
        self.current_NC = None  # it must be a string

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

