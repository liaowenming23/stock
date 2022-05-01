from mysql.connector import MySQLConnection
from src.models.stock_revenue_record import StockRevenueRecord
from src.repositories.sql_connector import MySqlConnector


class StockRevenueRecordRepository():

    def __init__(self, mysql_conn: MySqlConnector) -> None:
        self.db: MySQLConnection = mysql_conn.db

    def add(self, record: StockRevenueRecord):
        cursor = self.db.cursor()
        cursor.execute("""
            insert into stock_revenue (stock_id, `year`, `month`, revenue_by_million)
            values (%s, %s, %s, %s)
            """, (record.stock_id, record.year, record.month, record.revenue_by_million))
        self.db.commit()
        cursor.close()

    def check_exist_by_year_month(self, record: StockRevenueRecord):
        cursor = self.db.cursor()
        cursor.execute("""
            select id 
            from stock_revenue
            where stock_id = %s and `year` = %s and `month` = %s limit 1; 
            """, (record.stock_id, record.year, record.month))
        row = cursor.fetchone()
        return row is not None

    def get_revenue_by_stock_id(self, stock_id):
        cursor = self.db.cursor()
        cursor.execute("""
            select id, stock_id, `year`, `month`, revenue_by_million
            from stock_revenue
            where stock_id = %s; 
            """, (stock_id,))

        rows = cursor.fetchall()
        if rows is None:
            return None
        records: list[StockRevenueRecord] = []
        for row in rows:
            record = StockRevenueRecord()
            record.id = row[0]
            record.stock_id = row[1]
            record.year = row[2]
            record.month = row[3]
            record.revenue_by_million = row[4]
            records.append(record)
        return records
