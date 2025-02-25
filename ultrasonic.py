mport time
import math
import RPi.GPIO as GPIO
import os

class Measurement:
    def __init__(self, trig_pin, echo_pin, temperature=20, unit='metric', round_to=1, gpio_mode=GPIO.BCM):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        self.temperature = temperature
        self.unit = unit
        self.round_to = round_to
        self.gpio_mode = gpio_mode

        GPIO.setwarnings(False)
        GPIO.setmode(self.gpio_mode)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def raw_distance(self, sample_size=11, sample_wait=0.1):
        if self.unit == 'imperial':
            self.temperature = (self.temperature - 32) * 0.5556

        speed_of_sound = 331.3 * math.sqrt(1 + (self.temperature / 273.15))
        sample = []

        for _ in range(sample_size):
            GPIO.output(self.trig_pin, GPIO.LOW)
            time.sleep(sample_wait)
            GPIO.output(self.trig_pin, True)
            time.sleep(0.00001)
            GPIO.output(self.trig_pin, False)

            sonar_signal_off = None
            sonar_signal_on = None

            start_time = time.time()
            while GPIO.input(self.echo_pin) == 0:
                sonar_signal_off = time.time()
                if sonar_signal_off - start_time > 0.02:  # Timeout efter 20ms
                    return None

            while GPIO.input(self.echo_pin) == 1:
                sonar_signal_on = time.time()
                if sonar_signal_on - sonar_signal_off > 0.02:  # Timeout efter 20ms
                    return None

            if sonar_signal_off and sonar_signal_on:
                time_passed = sonar_signal_on - sonar_signal_off
                distance_cm = time_passed * ((speed_of_sound * 100) / 2)
                sample.append(distance_cm)

        return sorted(sample)[sample_size // 2] if sample else None

# Filhantering
file_path = "/home/ulf/distance_sensor_tmp.log"
if not os.path.exists(file_path):
    with open(file_path, "w"):
        pass

def log_distance_data(distance):
    """Loggar mätdata till filen och håller den under 5000 rader."""
    if distance is None:
        return  # Skippa loggning om ingen mätning gjorts
    
    with open(file_path, "a") as file:
        file.write(f"{distance}\n")

    # Håll endast de senaste 5000 raderna
    with open(file_path, "r") as file:
        lines = file.readlines()
    if len(lines) > 5000:
        with open(file_path, "w") as file:
            file.writelines(lines[-5000:])

sensor = Measurement(trig_pin=13, echo_pin=19)

previous_distance = None
tolerance = 5.0  # Toleransnivå

try:
    while True:
        distance = sensor.raw_distance()
        if distance is not None:
            distance_rounded = round(distance, 1)

            if previous_distance is None or abs(previous_distance - distance_rounded) > tolerance:
#                print(f"Avstånd: {distance_rounded} cm")
                log_distance_data(distance_rounded)
                previous_distance = distance_rounded

        time.sleep(16)

except KeyboardInterrupt:
    print("Programmet avslutades av användaren")
finally:
    GPIO.cleanup()
