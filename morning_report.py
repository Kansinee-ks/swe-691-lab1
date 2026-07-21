import os
import sys
import requests
from datetime import date, timedelta
from dotenv import load_dotenv
from sales_logger import get_sheet

load_dotenv()

def summarize_for_date(rows: list[dict], target_date: str) -> dict:
    day_rows = [r for r in rows if r["วันที่"] == target_date]
    total_sales = sum(float(r["ยอดรวม"]) for r in day_rows)
    total_items = sum(int(r["จำนวน"]) for r in day_rows)
    return {
        "date": target_date,
        "orders": len(day_rows),
        "items": total_items,
        "total": total_sales,
    }

def send_telegram(message: str, dry_run: bool = False):
    if dry_run:
        print(f"[DRY RUN] would send: {message}")
        return
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    resp = requests.post(url, data={"chat_id": chat_id, "text": message})
    resp.raise_for_status()

def main(dry_run: bool = False):
    sheet = get_sheet()
    rows = sheet.get_all_records()
    yesterday = str(date.today() - timedelta(days=1))
    summary = summarize_for_date(rows, yesterday)

    message = (
        f"📊 สรุปยอดขายวันที่ {summary['date']}\n"
        f"ออเดอร์: {summary['orders']}\n"
        f"จำนวนสินค้า: {summary['items']}\n"
        f"ยอดรวม: {summary['total']:.2f} บาท"
    )
    send_telegram(message, dry_run=dry_run)
    print(message)

if __name__ == "__main__":
    main(dry_run="--dry-run" in sys.argv)