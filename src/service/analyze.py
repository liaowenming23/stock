from datetime import datetime
from functools import reduce
from itertools import groupby
import typing
from src.models.stock_info import StockInfo
from src.models.stock_revenue_record import StockRevenueRecord
from src.repositories.sql_connector import MySqlConnector
from src.repositories.stock_info_repository import StockInfoRepository
from src.repositories.stock_revenue_repository import StockRevenueRecordRepository


def compare_year_average(records: list[StockRevenueRecord], stock_info: StockInfo):
    now = datetime.now()

    sorted_records = sorted(records, key=lambda r: r.year)
    records_group_by_year = {}
    for year, result in groupby(sorted_records, key=lambda r: r.year):
        records_group_by_year.setdefault(year, list(result))
    average_revenue_by_year: typing.Dict[str, int] = {}
    for k, rs in records_group_by_year.items():
        avg = reduce(lambda a, b: a+b,
                     [x.revenue_by_million for x in rs]) / len(rs)
        average_revenue_by_year.setdefault(str(k), avg)
    # print(average_revenue_by_year)
    years = ["2021"]
    this_avg_revenue = average_revenue_by_year.get(str(now.year))

    for y in years:
        r = average_revenue_by_year.get(y)
        r_p = this_avg_revenue / r
        if r_p > 1.1:
            print(stock_info.__dict__)
            print(f"growth percent:{r_p}")
    pass


def get_profitable_growth(rep: StockRevenueRecordRepository, stock_info: StockInfo):
    records = rep.get_revenue_by_stock_id(stock_id=stock_info.id)
    if len(records) == 0:
        # print("not records stock info")
        # print(stock_info.__dict__)
        return
    compare_year_average(records, stock_info)


def main():
    conntor = MySqlConnector("localhost", "stock", "root", "wenming01")
    stock_info_rep = StockInfoRepository(conntor)
    # stock_infos = stock_info_rep.get_stock_info_by_industry_type(2)
    stock_infos = stock_info_rep.get_all_stock_info()
    stock_revenue_rep = StockRevenueRecordRepository(conntor)
    # s = stock_info_rep.get_stock_info_by_stock_code("1101")
    # get_profitable_growth(stock_revenue_rep, s)
    for stock_info in stock_infos:
        get_profitable_growth(stock_revenue_rep, stock_info)


if __name__ == "__main__":
    main()
