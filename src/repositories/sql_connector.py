import mysql.connector
from mysql.connector import MySQLConnection


class MySqlConnector(object):
    def __init__(self, host: str, database: str, user: str, password: str) -> None:
        self.db: MySQLConnection = mysql.connector.connect(
            host=host, database=database, user=user, password=password)
