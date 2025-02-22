import requests
import time

# ThingSpeak API-uppgifter
THINGSPEAK_URL = "https://api.thingspeak.com/update"
API_KEY_TILT = "SRX5SYFZ66J2LV6T"  # Ersätt med din API-nyckel för tilt
API_KEY_DISTANCE = "2WICZMHK625MBB4D"  # Ersätt med din API-nyckel för avstånd

# Filvägar
tilt_log = "/home/ulf/tilt-sensor_tmp.log"
distance_log = "/home/ulf/distance_sensor_tmp.log"

def clear_log(file_path):
    """Rensar innehållet i en loggfil."""
    with open(file_path, "w"):
        pass  # Töm filen genom att öppna den för skrivning utan att skriva något

def read_last_line(file_path):
    """Läser den senaste raden från en fil."""
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            return lines[-1].strip() if lines else None
    except FileNotFoundError:
        return None

def send_to_thingspeak(api_key, field, value):
    """Skickar data till ThingSpeak."""
    payload = {'api_key': api_key, field: value}
    try:
        response = requests.post(THINGSPEAK_URL, data=payload)
        if response.status_code == 200:
            print(f"Data skickad till ThingSpeak: {field} = {value}")
        else:
            print(f"Fel vid sändning: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"HTTP-fel: {e}")

# Rensa loggfiler innan starten av huvudloopen
clear_log(tilt_log)
clear_log(distance_log)

# Huvudloop för att skicka data var 3:e sekund
while True:
    tilt_data = read_last_line(tilt_log)
    distance_data = read_last_line(distance_log)

    # Skriv ut senaste data från loggarna till terminalen
    if tilt_data:
        print(f"Senaste tilt data: {tilt_data}")
        send_to_thingspeak(API_KEY_TILT, 'field1', tilt_data)
    if distance_data:
        print(f"Senaste distance data: {distance_data}")
        send_to_thingspeak(API_KEY_DISTANCE, 'field1', distance_data)

    time.sleep(3)

