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
    try:
        cursor.execute(change(query))
        result = []
        if get_first(new_query) == 's' or get_first(new_query) == 'S':
            result = cursor.fetchall()
    finally:
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
        lens = []
        for t in header:
            lens.append(len(t))

        new_table = []
        for row in table:
            new_row = []
            for i in range(len(row)):
                new_row.append(str(row[i]))
                lens[i] = max(lens[i], len(new_row[i]))
            new_table.append(new_row)

        format_row = ""
        for l in lens:
            format_row += '{:>' + str(l + 2) + '}'

        print(format_row.format(*header))

        for row in table:
            print(format_row.format(*new_row))
