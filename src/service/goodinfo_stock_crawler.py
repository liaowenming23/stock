import requests
from bs4 import BeautifulSoup, Tag
GOODINFO_URL = "https://goodinfo.tw/tw/ShowSaleMonChart.asp?STOCK_ID={0}"


def get_sale_month(stock_code: str):
    url = GOODINFO_URL.format(stock_code)
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29"
    }
    resp = requests.get(url, headers=headers)
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, "lxml")
    table = soup.find("div", {"id": "divDetail"})
    for row in table.find_all("tr", {"align": "center"}):
        cols = row.find_all("nobr")
        print("date" + cols[0].text)
        
        print("開盤" + cols[1].text)
        print("營收" + cols[7].text)


def get_stock_code():
    pass


def spider():
    stock_code_list = ["1101"]
    for code in stock_code_list:
        get_sale_month(code)
        # sleep


def main():
    spider()
    pass


if __name__ == "__main__":
    main()
