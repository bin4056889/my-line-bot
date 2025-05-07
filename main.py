import requests

LINE_TOKEN = 'YOUR_LINE_ACCESS_TOKEN'
LINE_USER_ID = 'YOUR_USER_ID'
SHEET_API_URL = 'YOUR_GOOGLE_SCRIPT_WEB_APP_URL'

def get_data():
    response = requests.get(SHEET_API_URL)
    return response.json()

def format_message(data):
    msg = '"บน"\n'
    for i, row in enumerate(data["บน"]):
        msg += f'แถวที่ {i+1}"{row["เลข"]}" = {row["ค่า"]}\n'

    msg += '\n"ล่าง"\n'
    for i, row in enumerate(data["ล่าง"]):
        msg += f'แถวที่ {i+1}"{row["เลข"]}" = {row["ค่า"]}\n'

    msg += '\n"โต๊ด"\n'
    for i, row in enumerate(data["โต๊ด"]):
        msg += f'แถวที่ {i+1}"{row["เลข"]}" = {row["ค่า"]}\n'

    return msg

def push_line_message(text):
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_TOKEN}'
    }
    body = {
        'to': LINE_USER_ID,
        'messages': [{'type': 'text', 'text': text}]
    }
    requests.post(url, headers=headers, json=body)

# MAIN
data = get_data()
msg = format_message(data)
push_line_message(msg)
