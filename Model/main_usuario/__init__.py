""""
    Este modulo es exclusivo para las operaciones que debe de realizar un usuario iHealth+
"""

from Control.function_validation import *

class Usuario:

    def __init__(self, id):
        self.id = id

    def get_id(self):
        return self.id

    # https://www.w3schools.com/python/python_classes.asp
    # https://www.psycopg.org/docs/cursor.html#cursor.fetchone
    # https://www.tutorialspoint.com/postgresql/postgresql_python.htm
    # https://towardsdatascience.com/python-and-postgresql-how-to-access-a-postgresql-database-like-a-data-scientist-b5a9c5a0ea43
    