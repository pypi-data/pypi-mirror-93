from __future__ import annotations

from dataclasses import dataclass
from json import JSONEncoder
from typing import Optional


@dataclass
class Candle:
    current: float = 0.0
    open: float = 0.0
    close: float = 0.0
    high: float = 0.0
    low: float = 0.0
    day_high: Optional[float] = None
    day_low: Optional[float] = None
    day_open: Optional[float] = None


class CandleEncoder(JSONEncoder):
    def default(self, other):
        return other.__dict__


def main() -> None:
    candle = Candle(current=1.0, open=1.0, close=2.0, high=4.0, low=0.5, day_high=None, day_low=None, day_open=None)
    print(candle)


if __name__ == "__main__":
    main()
