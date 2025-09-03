"""
抓取懂车帝新车列表（更健壮的实现）
- 用 requests + 正则解析内嵌 JSON（更轻量）
- 增加重试、超时、异常处理和日志
- 将逻辑封装为函数并支持命令行参数与输出保存
"""

import re
import json
import csv
import argparse
import logging
from typing import Any, Dict, List, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


LOGGER = logging.getLogger(__name__)


def make_session(retries: int = 3, backoff: float = 0.3, timeout: int = 10) -> requests.Session:
    s = requests.Session()
    retries_strategy = Retry(
        total=retries,
        backoff_factor=backoff,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"],
    )
    adapter = HTTPAdapter(max_retries=retries_strategy)
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    })
    # store timeout on session for convenience
    s.request_timeout = timeout  # type: ignore[attr-defined]
    return s


def fetch_html(session: requests.Session, url: str) -> str:
    timeout = getattr(session, "request_timeout", 10)
    LOGGER.debug("Fetching URL %s with timeout=%s", url, timeout)
    resp = session.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.text


def extract_next_data(html: str) -> Optional[Dict[str, Any]]:
    m = re.search(r'<script id="__NEXT_DATA__" type="application/json" crossorigin="anonymous">(.*?)</script>', html, re.DOTALL)
    if not m:
        LOGGER.debug("__NEXT_DATA__ script tag not found")
        return None
    try:
        payload = m.group(1)
        return json.loads(payload)
    except json.JSONDecodeError as e:
        LOGGER.exception("Failed to decode JSON from __NEXT_DATA__: %s", e)
        return None


def parse_series_list(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    # Navigate safely through nested keys
    try:
        series_list = data.get("props", {}).get("pageProps", {}).get("series_list", [])
    except Exception:
        LOGGER.exception("Unexpected data format when extracting series_list")
        return []

    result = []
    for series in series_list:
        item = {
            "series_name": series.get("series_name"),
            "price": series.get("price_info", {}).get("price"),
            "online_date": f"{series.get('online_date_month')}月{series.get('online_date_day')}日",
            "tags": [t.get("name") for t in series.get("tag_list", []) if t.get("name")],
        }
        result.append(item)
    return result


def save_json(data: List[Dict[str, Any]], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    LOGGER.info("Saved %d items to %s", len(data), path)


def save_csv(data: List[Dict[str, Any]], path: str) -> None:
    if not data:
        LOGGER.info("No data to write to CSV")
        return
    keys = list(data[0].keys())
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for row in data:
            # flatten tags list to a semicolon-separated string
            row_copy = row.copy()
            if isinstance(row_copy.get("tags"), list):
                row_copy["tags"] = ";".join(row_copy["tags"])
            writer.writerow(row_copy)
    LOGGER.info("Saved CSV to %s", path)


def main() -> int:
    parser = argparse.ArgumentParser(description="爬取懂车帝新车列表并保存")
    parser.add_argument("--url", default="https://www.dongchedi.com/newcar", help="目标页面 URL")
    parser.add_argument("--out", default="dongchedi_newcars.json", help="输出 JSON 文件路径")
    parser.add_argument("--csv", default=None, help="可选：输出 CSV 文件路径")
    parser.add_argument("--timeout", type=int, default=10, help="请求超时时间（秒）")
    parser.add_argument("--retries", type=int, default=3, help="重试次数")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    session = make_session(retries=args.retries, timeout=args.timeout)

    try:
        html = fetch_html(session, args.url)
    except requests.RequestException as e:
        LOGGER.exception("Request failed: %s", e)
        return 2

    data = extract_next_data(html)
    if data is None:
        LOGGER.error("Failed to find or parse __NEXT_DATA__ in the page")
        return 3

    items = parse_series_list(data)
    if not items:
        LOGGER.warning("No series items extracted")

    # Print summary to console
    for it in items:
        print(f"新车发布：{it.get('series_name')}")
        print(f"售价范围：{it.get('price')}")
        print(f"上市时间：{it.get('online_date')}")
        if it.get('tags'):
            print("上新类型：", ",".join(it.get('tags')))
        print("-" * 30)

    # Save outputs
    try:
        save_json(items, args.out)
        if args.csv:
            save_csv(items, args.csv)
    except OSError:
        LOGGER.exception("Failed to write output files")
        return 4

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

