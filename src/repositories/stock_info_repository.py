from mysql.connector import MySQLConnection
from src.models.stock_info import StockInfo
from src.repositories.sql_connector import MySqlConnector


class StockInfoRepository():

    def __init__(self, mysql_conn: MySqlConnector) -> None:
        self.db: MySQLConnection = mysql_conn.db

    def add_stock_info(self, stock_info: StockInfo):
        cursor = self.db.cursor()
        cursor.execute("""
            insert into `stock_info` (stock_code, stock_name, industry_type, create_time)
            values (%s, %s, %s, %s)
            """, (stock_info.stock_code, stock_info.stock_name, stock_info.industry_type, stock_info.create_time))
        self.db.commit()
        cursor.close()

    def get_stock_info_by_stock_code(self, stock_code: str) -> StockInfo:
        cursor = self.db.cursor()
        cursor.execute("""
            select id, stock_code, stock_name, industry_type, create_time
            from `stock_info`
            where stock_code = %s limit 1;
           """, (stock_code,))
        row = cursor.fetchone()
        if row is None:
            return None
        stock_info = StockInfo()
        stock_info.id = int(row[0])
        stock_info.stock_code = str(row[1])
        stock_info.stock_name = str(row[2])
        stock_info.industry_type = int(row[3])
        stock_info.create_time = row[4]
        cursor.close()
        return stock_info

    def get_stock_info_by_industry_type(self, industry_type: int):
        cursor = self.db.cursor()
        cursor.execute("""
            select id, stock_code, stock_name, industry_type, create_time
            from `stock_info`
            where industry_type = %s;
           """, (industry_type,))
        rows = cursor.fetchall()
        if rows is None:
            return None
        stock_infos: list[StockInfo] = []
        for row in rows:
            stock_info = StockInfo()
            stock_info.id = int(row[0])
            stock_info.stock_code = str(row[1])
            stock_info.stock_name = str(row[2])
            stock_info.industry_type = int(row[3])
            stock_info.create_time = row[4]
            stock_infos.append(stock_info)
        cursor.close()
        return stock_infos

    def get_all_stock_info(self):
        cursor = self.db.cursor()
        cursor.execute("""
            select id, stock_code, stock_name, industry_type, create_time
            from `stock_info`;
           """,)
        rows = cursor.fetchall()
        if rows is None:
            return None
        stock_infos: list[StockInfo] = []
        for row in rows:
            stock_info = StockInfo()
            stock_info.id = int(row[0])
            stock_info.stock_code = str(row[1])
            stock_info.stock_name = str(row[2])
            stock_info.industry_type = int(row[3])
            stock_info.create_time = row[4]
            stock_infos.append(stock_info)
        cursor.close()
        return stock_infos


def main():
    conntor = MySqlConnector("localhost", "stock", "root", "wenming01")
    rep = StockInfoRepository(conntor)
    # stock_info = StockInfo()
    # stock_info.stock_code = "1101"
    # stock_info.stock_name = "??????"
    # stock_info.industry_type = 1
    # stock_info.create_time = datetime.now()
    # rep.add_stock_info(stock_info)
    stock_info = rep.get_stock_info_by_stock_code("1101")
    print(stock_info.__dict__)


if __name__ == "__main__":
    main()
