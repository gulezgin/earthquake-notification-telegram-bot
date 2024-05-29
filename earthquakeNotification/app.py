import requests
from bs4 import BeautifulSoup
import time

def send_telegram_message(message):
    telegram_api_url = "https://api.telegram.org/bot{}/sendMessage".format(telegram_bot_token)
    requests.post(telegram_api_url, data={"chat_id": telegram_chat_id, "text": message})

def get_latest_earthquakes():
    url = "https://deprem.afad.gov.tr/last-earthquakes.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find("table")
    rows = table.find_all("tr")

    latest_earthquakes = []

    for row in rows[:10]:
        cells = row.find_all("td")
        if cells:
            date = cells[0].text.strip()
            magnitude = float(cells[5].text.strip())
            location = cells[6].text.strip()
            eq_id = cells[7].text.strip()

            if magnitude > 4.0 and eq_id not in kutuphane:
                latest_earthquakes.append({"date": date, "magnitude": magnitude, "location": location})
                kutuphane.append(eq_id)

    return latest_earthquakes

def format_earthquake_message(earthquake):
    message = "🚨 Yeni Deprem !\n"
    message += "🗺️ Yer: {}\n".format(earthquake["location"])
    message += "🔴 Büyüklük: {}\n".format(earthquake["magnitude"])
    message += "📅 Tarih: {}\n".format(earthquake["date"])
    message += "🟡 Kaynak: AFAD"
    return message

if __name__ == "__main__":
    kutuphane = []
    telegram_bot_token = ""
    telegram_chat_id = ""

    while True:
        latest_earthquakes = get_latest_earthquakes()
        for earthquake in latest_earthquakes:
            message = format_earthquake_message(earthquake)
            send_telegram_message(message)
        time.sleep(120)
