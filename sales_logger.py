import os
import sys
from datetime import date
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def get_sheet():
    creds = Credentials.from_service_account_file(
        os.environ.get("GOOGLE_SERVICE_ACCOUNT_FILE", "credentials.json"),
        scopes=SCOPES,
    )
    gc = gspread.authorize(creds)
    return gc.open_by_key(os.environ["GOOGLE_SHEETS_ID"]).sheet1

def log_sale(menu: str, qty: int, price: float, sheet=None):
    sheet = sheet or get_sheet()
    total = qty * price
    row = [str(date.today()), menu, qty, price, total]
    sheet.append_row(row)
    return row

if __name__ == "__main__":
    menu = sys.argv[1]
    qty = int(sys.argv[2])
    price = float(sys.argv[3])
    row = log_sale(menu, qty, price)
    print(f"Logged: {row}")