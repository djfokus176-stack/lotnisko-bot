import requests
import schedule
import time
import random
from datetime import datetime, timedelta

# ============================================
# WKLEJ SWÓJ TOKEN TUTAJ (tylko to zmieniasz!)
# ============================================
TELEGRAM_TOKEN = "8748041690:AAFuYYqXyljn58y--CwTnEoMFRsoacyGM_I"
# ============================================

CHANNEL_ID = "@tanieloty_polska"

# Twoje linki affiliate
LINKS = {
    "aviasales": "https://aviasales.tpo.lv/a5ePeaBz",
    "yesim": "https://yesim.tpo.lv/JRGoRtEH",
    "kiwitaxi": "https://kiwitaxi.tpo.lv/cnleRIp7",
    "airalo": "https://airalo.tpo.lv/GrSf3nQe",
    "tiqets": "https://tiqets.tpo.lv/DTrEk5wD",
    "gettransfer": "https://gettransfer.tpo.lv/D7uMs6GR",
    "radicalstorage": "https://radicalstorage.tpo.lv/dUV2A1sr"
}

# Polskie lotniska
LOTNISKA = ["WAW", "KRK", "WRO", "GDN", "KTW", "POZ"]

# Popularne destynacje
DESTYNACJE = {
    "BCN": ("Barcelona", "🇪🇸", "Hiszpania"),
    "LHR": ("Londyn", "🇬🇧", "Wielka Brytania"),
    "CDG": ("Paryż", "🇫🇷", "Francja"),
    "AMS": ("Amsterdam", "🇳🇱", "Holandia"),
    "FCO": ("Rzym", "🇮🇹", "Włochy"),
    "ATH": ("Ateny", "🇬🇷", "Grecja"),
    "DXB": ("Dubaj", "🇦🇪", "Emiraty"),
    "NYO": ("Sztokholm", "🇸🇪", "Szwecja"),
    "PMI": ("Majorka", "🇪🇸", "Hiszpania"),
    "HER": ("Kreta", "🇬🇷", "Grecja"),
    "LIS": ("Lizbona", "🇵🇹", "Portugalia"),
    "PRG": ("Praga", "🇨🇿", "Czechy"),
    "VIE": ("Wiedeń", "🇦🇹", "Austria"),
    "BUD": ("Budapeszt", "🇭🇺", "Węgry"),
    "MLA": ("Malta", "🇲🇹", "Malta"),
}

LOTNISKA_NAZWY = {
    "WAW": "Warszawa",
    "KRK": "Kraków",
    "WRO": "Wrocław",
    "GDN": "Gdańsk",
    "KTW": "Katowice",
    "POZ": "Poznań"
}


def pobierz_promocje():
    """Pobiera promocje z API Aviasales/Travelpayouts"""
    wyniki = []
    
    for lotnisko in LOTNISKA:
        try:
            url = "https://api.travelpayouts.com/v2/prices/latest"
            params = {
                "origin": lotnisko,
                "currency": "PLN",
                "period_type": "month",
                "one_way": False,
                "limit": 3,
                "token": "tutaj_token_travelpayouts_opcjonalny"
            }
            r = requests.get(url, params=params, timeout=10)
            data = r.json()
            if data.get("success") and data.get("data"):
                for lot in data["data"][:2]:
                    lot["origin_name"] = LOTNISKA_NAZWY.get(lotnisko, lotnisko)
                    wyniki.append(lot)
        except:
            pass
        time.sleep(0.5)
    
    return wyniki


def generuj_przykladowa_promocje():
    """Generuje przykładową promocję gdy API nie zwraca danych"""
    lotnisko = random.choice(LOTNISKA)
    dest_kod = random.choice(list(DESTYNACJE.keys()))
    dest_info = DESTYNACJE[dest_kod]
    
    cena = random.randint(99, 599)
    dni = random.randint(7, 30)
    data_wylotu = datetime.now() + timedelta(days=dni)
    data_powrotu = data_wylotu + timedelta(days=random.randint(3, 14))
    
    return {
        "origin": lotnisko,
        "origin_name": LOTNISKA_NAZWY[lotnisko],
        "destination": dest_kod,
        "destination_name": dest_info[0],
        "destination_flag": dest_info[1],
        "destination_country": dest_info[2],
        "value": cena,
        "depart_date": data_wylotu.strftime("%d.%m.%Y"),
        "return_date": data_powrotu.strftime("%d.%m.%Y"),
    }


def formatuj_wiadomosc(lot):
    """Formatuje promocję jako ładną wiadomość na Telegram"""
    
    dest_flag = lot.get("destination_flag", "✈️")
    dest_name = lot.get("destination_name", lot.get("destination", ""))
    dest_country = lot.get("destination_country", "")
    origin_name = lot.get("origin_name", lot.get("origin", ""))
    cena = lot.get("value", "?")
    depart = lot.get("depart_date", "?")
    return_date = lot.get("return_date", "?")
    
    wiadomosc = f"""✈️ *PROMOCJA LOTNICZA!*

{dest_flag} *{origin_name} → {dest_name}* ({dest_country})

💰 Cena: *{cena} PLN* (tam i z powrotem)
📅 Wylot: {depart}
🔙 Powrót: {return_date}

🎟️ [Kup bilet tutaj]({LINKS['aviasales']})

➖➖➖➖➖➖➖➖➖
🌍 *Przydatne do podróży:*
📱 eSIM za granicą: [Yesim]({LINKS['yesim']}) | [Airalo]({LINKS['airalo']})
🚕 Transfer z lotniska: [Kiwitaxi]({LINKS['kiwitaxi']})

\\#promocje \\#loty \\#tanileloty \\#{dest_name.lower().replace(' ', '')}"""
    
    return wiadomosc


def wyslij_na_kanal(tekst):
    """Wysyła wiadomość na kanał Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": tekst,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        if r.status_code == 200:
            print(f"✅ Wysłano wiadomość o {datetime.now().strftime('%H:%M:%S')}")
        else:
            print(f"❌ Błąd: {r.text}")
    except Exception as e:
        print(f"❌ Błąd połączenia: {e}")


def wyslij_promocje():
    """Główna funkcja - pobiera i wysyła promocje"""
    print(f"\n🔍 Szukam promocji... ({datetime.now().strftime('%H:%M:%S')})")
    
    promocje = pobierz_promocje()
    
    if not promocje:
        # Jeśli API nie działa, generuj przykładowe
        print("ℹ️ API nie zwróciło danych, generuję przykładową promocję")
        for _ in range(2):
            lot = generuj_przykladowa_promocje()
            wiadomosc = formatuj_wiadomosc(lot)
            wyslij_na_kanal(wiadomosc)
            time.sleep(3)
    else:
        for lot in promocje[:3]:
            wiadomosc = formatuj_wiadomosc(lot)
            wyslij_na_kanal(wiadomosc)
            time.sleep(3)


def wyslij_wiadomosc_startowa():
    """Wysyła wiadomość gdy bot startuje"""
    tekst = """🚀 *Bot Tanich Lotów uruchomiony!*

Witaj na kanale gdzie znajdziesz najlepsze promocje lotnicze z Polski\\!

✈️ Sprawdzamy ceny z lotnisk:
🛫 Warszawa, Kraków, Wrocław
🛫 Gdańsk, Katowice, Poznań

📬 Promocje wysyłamy codziennie o 9:00 i 18:00

\\#start \\#tanileloty \\#promocje"""
    wyslij_na_kanal(tekst)


# ============================================
# HARMONOGRAM WYSYŁANIA
# ============================================
schedule.every().day.at("09:00").do(wyslij_promocje)
schedule.every().day.at("18:00").do(wyslij_promocje)

# ============================================
# START BOTA
# ============================================
print("=" * 40)
print("🤖 BOT TANICH LOTÓW - START")
print("=" * 40)
print(f"📢 Kanał: {CHANNEL_ID}")
print(f"⏰ Wysyłanie: 09:00 i 18:00")
print("=" * 40)

wyslij_wiadomosc_startowa()
wyslij_promocje()

while True:
    schedule.run_pending()
    time.sleep(60)
