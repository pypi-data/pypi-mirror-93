from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Lot:
    id: str
    symbol: str
    shares: float
    purchase_price: float
    notes: str
    purchase_time: datetime
    investment_strategy_data: str
    profit_loss: float
    rid: Optional[str] = None
