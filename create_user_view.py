import psycopg2
from psycopg2 import Error


def execute_create_view_query(cursor, query, view_name):
    try:
        cursor.execute(query)
    except (Exception, Error) as error:
        print("Error While Creating(View) " + view_name, error)