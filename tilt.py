import RPi.GPIO as GPIO
import time

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
