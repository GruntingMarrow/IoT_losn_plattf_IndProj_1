import RPi.GPIO as GPIO
import time
import os

# Sätt upp GPIO-läge
GPIO.setmode(GPIO.BCM)

# Pinnar för tilt-sensor och LED-dioder
tilt_pin = 25  # DO-pinnen för tilt-sensor
green_led_pin = 24  # Grön LED för inte tiltad
red_led_pin = 23  # Röd LED för tilltad

# Sätt upp pins som ingång eller utgång
GPIO.setup(tilt_pin, GPIO.IN)
GPIO.setup(green_led_pin, GPIO.OUT)
GPIO.setup(red_led_pin, GPIO.OUT)

# Filens sökväg
file_path = "/home/ulf/tilt-sensor_tmp.log"

# Skapa filen om den inte finns
if not os.path.exists(file_path):
    with open(file_path, "w"):
        pass

def log_sensor_data(state):
    """Loggar sensordata i en temporär fil."""
    with open(file_path, "a") as file:
        file.write(f"{state}\n")  # Logga 0 eller 1

    # Håll filen under 100 rader
    with open(file_path, "r") as file:
        lines = file.readlines()
    if len(lines) > 100:
        with open(file_path, "w") as file:
            file.writelines(lines[-100:])

# Håll koll på det senaste tillståndet
last_state = None

try:
    while True:
        # Läs av om sensorn är tiltad eller inte
        current_state = GPIO.input(tilt_pin)  # 0 = Tiltad, 1 = Ej tiltad


        # Om tillståndet har förändrats, skriv ut och uppdatera LED-status
        if current_state != last_state:
            if current_state == GPIO.HIGH:
                GPIO.output(green_led_pin, GPIO.HIGH)  # Tänd grön LED
                GPIO.output(red_led_pin, GPIO.LOW)    # Släck röd LED
                log_sensor_data(0)  # Ej tiltad = 0
            else:
                GPIO.output(green_led_pin, GPIO.LOW)  # Släck grön LED
                GPIO.output(red_led_pin, GPIO.HIGH)   # Tänd röd LED
                log_sensor_data(1)  # Tiltad = 1

            last_state = current_state  # Uppdatera senaste tillståndet

        time.sleep(15)  # Vänta innan nästa läsning

except KeyboardInterrupt:
    print("Programmet avslutades av användaren")
    GPIO.cleanup()

