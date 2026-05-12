from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from typing import Callable, Optional
from urllib.request import urlopen

DEFAULT_API_URL = "https://api.gold-api.com/price/XAU"


def fetch_gold_price(api_url: str = DEFAULT_API_URL, timeout: int = 10) -> float:
    with urlopen(api_url, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))

    if "price" not in payload:
        raise ValueError("Gold price response does not contain 'price'")

    return float(payload["price"])


def build_reminder_message(
    price: float,
    currency: str = "USD",
    threshold: Optional[float] = None,
    now: Optional[datetime] = None,
) -> str:
    now = now or datetime.now(timezone.utc)
    base = f"[{now.strftime('%Y-%m-%d')}] 今日金价提醒：{price:.2f} {currency}/oz"

    if threshold is not None:
        if price >= threshold:
            return f"{base}，已达到你设置的提醒阈值 {threshold:.2f}。"
        return f"{base}，尚未达到提醒阈值 {threshold:.2f}。"

    return base


def run_daily_reminder(
    notifier: Callable[[str], None] = print,
    api_url: str = DEFAULT_API_URL,
    threshold: Optional[float] = None,
    mock_price: Optional[float] = None,
) -> str:
    price = mock_price if mock_price is not None else fetch_gold_price(api_url=api_url)
    message = build_reminder_message(price=price, threshold=threshold)
    notifier(message)
    return message


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="每日金价提醒 Agent")
    parser.add_argument("--api-url", default=DEFAULT_API_URL, help="金价 API 地址")
    parser.add_argument("--threshold", type=float, default=None, help="提醒阈值（USD/oz）")
    parser.add_argument(
        "--mock-price",
        type=float,
        default=None,
        help="本地验证用，直接使用该价格而不是请求 API",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_daily_reminder(
        api_url=args.api_url,
        threshold=args.threshold,
        mock_price=args.mock_price,
    )


if __name__ == "__main__":
    main()
