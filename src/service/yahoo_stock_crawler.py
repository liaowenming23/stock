from datetime import datetime
import requests
from bs4 import BeautifulSoup, Tag
from src.models.stock_info import IndustryType, StockInfo
from src.repositories.sql_connector import MySqlConnector
from src.repositories.stock_info_repository import StockInfoRepository


def get_stock_info_list() -> list[StockInfo]:
    url = "https://tw.stock.yahoo.com/h/kimosel.php?tse=1&cat=%E5%8D%8A%E5%B0%8E%E9%AB%94&form=menu&form_id=stock_id&form_name=stock_name&domain=0"
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29"
    }
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text)
    table = soup.find("form", {"name": "stock"})
    stock_items = table.find_all("a", {"class": "none"})
    stock_list: list[StockInfo] = []
    for stock in stock_items:
        stock: Tag = stock
        val = stock.text.strip().split(' ')
        stock_code = val[0]
        stock_name = val[1]
        print("stock_code:"+stock_code)
        print("stock_name:"+stock_name)
        stock_info = StockInfo()
        stock_info.stock_code = stock_code
        stock_info.stock_name = stock_name
        stock_info.industry_type = IndustryType.Semiconductor.value
        stock_info.create_time = datetime.now()
        stock_list.append(stock_info)

    return stock_list


def main():
    stock_list = get_stock_info_list()
    conntor = MySqlConnector("localhost", "stock", "root", "wenming01")
    rep = StockInfoRepository(conntor)
    for s in stock_list:
        stock_info = rep.get_stock_info_by_stock_code(s.stock_code)
        if stock_info is None:
            rep.add_stock_info(s)
    pass


if __name__ == "__main__":
    main()