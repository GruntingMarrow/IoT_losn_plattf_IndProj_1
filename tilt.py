import RPi.GPIO as GPIO
import time
import os

# Sätt upp GPIO-läge
GPIO.setmode(GPIO.BCM)

# Pinnar för tilt-sensor och LED-dioder
tilt_pin = 25  # DO-pinnen för tilt-sensor
green_led_pin = 24  # Grön LED för inte tilltad
red_led_pin = 23  # Röd LED för tilltad

# Sätt upp pins som ingång eller utgång
GPIO.setup(tilt_pin, GPIO.IN)
GPIO.setup(green_led_pin, GPIO.OUT)
GPIO.setup(red_led_pin, GPIO.OUT)


# Filens sökväg
file_path = os.path.expanduser("~/tilt-sensor_tmp.log")

# **Skapa filen om den inte finns (touch-funktion)**
if not os.path.exists(file_path):
    open(file_path, "a").close()

def log_sensor_data(state):
    """Loggar sensordata i en temporär fil."""
    with open(file_path, "a") as file:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{timestamp}, {'Tiltad' if state == GPIO.LOW else 'Ej tiltad'}\n")

        # Håll filen under 100 rader
        file.seek(0)
        lines = file.readlines()
        if len(lines) > 100:
            with open(file_path, "w") as f:
                f.writelines(lines[-100:])

# Håll koll på det senaste tillståndet
last_state = None

try:
    while True:
        # Läs av om sensorn är tiltad eller inte
        current_state = GPIO.input(tilt_pin)

        # Om tillståndet har förändrats, skriv ut och uppdatera LED-status
        if current_state != last_state:
            if current_state == GPIO.HIGH:
                # Sensor är inte tiltad
                print("Sensor är inte tiltad")
                GPIO.output(green_led_pin, GPIO.HIGH)  # Tänd grön LED
                GPIO.output(red_led_pin, GPIO.LOW)    # Släck röd LED
            else:
                # Sensor är tiltad
                print("Sensor är tiltad")
                GPIO.output(green_led_pin, GPIO.LOW)  # Släck grön LED
                GPIO.output(red_led_pin, GPIO.HIGH)   # Tänd röd LED

            # Uppdatera senaste tillståndet
            last_state = current_state

        time.sleep(0.3)  # Vänta 0.5 sekunder innan nästa läsning

except KeyboardInterrupt:
    print("Programmet avslutades av användaren")
    GPIO.cleanup()
