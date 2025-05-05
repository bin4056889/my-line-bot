import gspread
import time
import pickle
import requests
from oauth2client.service_account import ServiceAccountCredentials

# === กำหนดค่าเบื้องต้น ===
LINE_TOKEN = "YOUR_LINE_NOTIFY_TOKEN"
SPREADSHEET_NAME = "YOUR_SPREADSHEET_NAME"
JSON_CREDENTIAL_PATH = "service_account.json"
LAST_ROW_FILE = "last_row.pkl"

# === STEP 1: เชื่อมต่อ Google Sheets ===
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_CREDENTIAL_PATH, scope)
client = gspread.authorize(creds)
sheet = client.open(SPREADSHEET_NAME).sheet1

# === STEP 2: โหลดสถานะแถวล่าสุดที่เคยดึง ===
def load_last_row():
    try:
        with open(LAST_ROW_FILE, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return 1  # เริ่มจากแถวที่ 2 (index 1)

# === STEP 3: บันทึกสถานะล่าสุดหลังส่งแล้ว ===
def save_last_row(row):
    with open(LAST_ROW_FILE, "wb") as f:
        pickle.dump(row, f)

# === STEP 4: ส่งข้อความไปยัง LINE Notify ===
def send_line_notify(message):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {LINE_TOKEN}"}
    data = {"message": message}
    r = requests.post(url, headers=headers, data=data)
    return r.status_code

# === STEP 5: ดึงข้อมูลใหม่และส่งไป LINE ===
def check_and_send():
    last_row = load_last_row()
    all_data = sheet.get_all_values()

    new_data = []
    for i in range(last_row, len(all_data)):
        row = all_data[i]
        if len(row) > 0 and row[0].strip() != "":
            new_data.append(row[0].strip())

    if new_data:
        message = "บน\n"
        for number in new_data:
            message += f"{number} = บน\n"
        send_line_notify(message.strip())

        save_last_row(last_row + len(new_data))

# === STEP 6: วนลูปทุก 5 นาที ===
if __name__ == "__main__":
    while True:
        check_and_send()
        time.sleep(300)
