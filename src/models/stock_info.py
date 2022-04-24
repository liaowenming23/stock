from datetime import datetime
from enum import Enum


class IndustryType(Enum):
    Semiconductor = 1  # 半導體


class StockInfo():
    def __init__(self) -> None:
        self.id: int
        self.stock_code: str
        self.stock_name: str
        self.industry_type: int
        self.create_time: datetime
