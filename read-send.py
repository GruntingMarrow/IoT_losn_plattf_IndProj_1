import requests
import time

# ThingSpeak API-url och din skriv-API-nyckel
THINGSPEAK_URL = "https://api.thingspeak.com/update"
API_KEY = "api"

# Filvägar för de temporära loggfilerna
tilt_file_path = "~/tilt-sensor_tmp.log"
distance_file_path = "~/distance_sensor_tmp.log"

# Läs data från filen
def read_data_from_file(file_path):
    """Läser den senaste raden från en fil."""
    file_path = os.path.expanduser(file_path)
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            if lines:
                return lines[-1].strip()  # Hämtar sista raden
            else:
                return None
    except FileNotFoundError:
        print(f"Filen {file_path} hittades inte.")
        return None

# Skicka data till ThingSpeak
def send_to_thingspeak(field1, field2):
    """Skickar data till ThingSpeak."""
    payload = {
        'api_key': API_KEY,
        'field1': field1,
        'field2': field2
    }
    try:
        response = requests.post(THINGSPEAK_URL, data=payload)
        if response.status_code == 200:
            print("Data skickad till ThingSpeak.")
        else:
            print(f"Fel vid att skicka data: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Fel vid HTTP-förfrågan: {e}")

# Huvudloop för att läsa och skicka data
while True:
    # Läs senaste data från varje fil
    tilt_data = read_data_from_file(tilt_file_path)
    distance_data = read_data_from_file(distance_file_path)

    # Om både data finns, skicka till ThingSpeak
    if tilt_data and distance_data:
        print(f"Skickar data: Tilt: {tilt_data}, Avstånd: {distance_data}")
        send_to_thingspeak(tilt_data, distance_data)

    # Vänta 60 sekunder innan nästa läsning
    time.sleep(1)
