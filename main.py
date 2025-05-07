import requests

LINE_TOKEN = 'V3PaJfhewTTKFmp8x7Ewn0lVP8yVMUjdOcbPz14U2SGPQy4NVJeCTo93v6Gpcne4WhaUfcQdEECnOz9RKlaHvDlhMg1DB1EDgRlBUzEfr8GveyVjbb+dzT6eh8v1Of3MA3FHYvvBxvTZNqMwUN2VegdB04t89/1O/w1cDnyilFU='
LINE_USER_ID = 'Uc56394608094708da3e9fcbf0f4e7778'
SHEET_API_URL = 'https://script.google.com/macros/s/AKfycby11NuRqjA2XrusxaUdvAKAK8tdox5NMxmsbG7j9kbU/dev'

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
