import time
import requests
from decimal import Decimal
from bs4 import BeautifulSoup, Tag
from src.models.stock_info import IndustryType, StockInfo
from src.models.stock_revenue_record import StockRevenueRecord
from src.repositories.sql_connector import MySqlConnector
from src.repositories.stock_info_repository import StockInfoRepository
from src.repositories.stock_revenue_repository import StockRevenueRecordRepository
GOODINFO_URL = "https://goodinfo.tw/tw/ShowSaleMonChart.asp?STOCK_ID={0}"


def get_monthly_revenue(stock_info: StockInfo):
    url = GOODINFO_URL.format(stock_info.stock_code)
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29"
    }
    resp = requests.get(url, headers=headers)
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, "lxml")
    table = soup.find("div", {"id": "divDetail"})
    records: list[StockRevenueRecord] = []
    for row in table.find_all("tr", {"align": "center"}):
        cols = row.find_all("nobr")
        record = StockRevenueRecord()
        record.stock_id = stock_info.id
        (year, month) = split_year_month(cols[0].text)
        record.year = int(year)
        record.month = int(month)
        record.revenue_by_million = int(
            Decimal(cols[7].text.replace(",", "")) * 100)
        print("date" + cols[0].text)
        print("營收" + cols[7].text)
        records.append(record)
    return records


def split_year_month(date: str):
    d = date.split("/")
    return (d[0], d[1])


def get_stock_code():
    pass


def add_to_database(conntor: MySqlConnector, records: list[StockRevenueRecord]):
    rep = StockRevenueRecordRepository(conntor)
    for record in records:
        if not rep.check_exist_by_year_month(record):
            rep.add(record)


def spider():
    conntor = MySqlConnector("localhost", "stock", "root", "wenming01")
    stock_info_rep = StockInfoRepository(conntor)
    stock_infos = stock_info_rep.get_stock_info_by_industry_type(
        IndustryType.Semiconductor.value)
    for stock_info in stock_infos:
        records = get_monthly_revenue(stock_info)
        add_to_database(conntor, records)
        time.sleep(5)


def main():
    spider()


if __name__ == "__main__":
    main()
