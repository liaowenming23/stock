from src.models.stock_industry import StockIndustry
from src.repositories.sql_connector import MySqlConnector


class StockIndustryRepository():

    def __init__(self, mysql_conn: MySqlConnector) -> None:
        self.db: MySqlConnector = mysql_conn.db

    def get_all_industry(self):
        cursor = self.db.cursor()
        cursor.execute("""
            select *
            from `stock_industry`
           """)
        rows = cursor.fetchall()
        if rows is None:
            return None
        industries: list[StockIndustry] = []
        for row in rows:
            industry = StockIndustry()
            industry.id = row[0]
            industry.name = row[1]
            industries.append(industry)
        return industries