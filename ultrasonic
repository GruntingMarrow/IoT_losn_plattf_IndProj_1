import time
import math
import RPi.GPIO as GPIO

class Measurement(object):
    '''Create a measurement using a HC-SR04 Ultrasonic Sensor connected to 
    the GPIO pins of a Raspberry Pi.'''

    def __init__(self,
                 trig_pin,
                 echo_pin,
                 temperature=20,
                 unit='metric',
                 round_to=1,
                 gpio_mode=GPIO.BCM):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        self.temperature = temperature
        self.unit = unit
        self.round_to = round_to
        self.gpio_mode = gpio_mode

    def raw_distance(self, sample_size=11, sample_wait=0.1):
        '''Return an error corrected unrounded distance, in cm, of an object 
        adjusted for temperature in Celcius.'''

        if self.unit == 'imperial':
            self.temperature = (self.temperature - 32) * 0.5556
        elif self.unit == 'metric':
            pass
        else:
            raise ValueError('Wrong Unit Type. Unit Must be imperial or metric')

        speed_of_sound = 331.3 * math.sqrt(1+(self.temperature / 273.15))
        sample = []
        # setup input/output pins
        GPIO.setwarnings(False)
        GPIO.setmode(self.gpio_mode)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

        for distance_reading in range(sample_size):
            GPIO.output(self.trig_pin, GPIO.LOW)
            time.sleep(sample_wait)
            GPIO.output(self.trig_pin, True)
            time.sleep(0.00001)
            GPIO.output(self.trig_pin, False)
            echo_status_counter = 1
            try:
                while GPIO.input(self.echo_pin) == 0:
                    if echo_status_counter < 1000:
                        sonar_signal_off = time.time()
                        echo_status_counter += 1
                    else:
                        raise SystemError('Echo pulse was not received')
                while GPIO.input(self.echo_pin) == 1:
                    sonar_signal_on = time.time()
                time_passed = sonar_signal_on - sonar_signal_off
                distance_cm = time_passed * ((speed_of_sound * 100) / 2)
                sample.append(distance_cm)
            except SystemError:
                print("No echo received. Skipping this reading.")
                return None
        sorted_sample = sorted(sample)
        # Only cleanup the pins used to prevent clobbering
        # any others in use by the program
        GPIO.cleanup((self.trig_pin, self.echo_pin))
        return sorted_sample[sample_size // 2]

    def distance_metric(self, median_reading):
        '''Calculate the rounded metric distance, in cm's, from the sensor to an object'''
        return round(median_reading, self.round_to)

sensor = Measurement(trig_pin=13, echo_pin=19)

# Första värdet som ska jämföras
previous_distance = None
tolerance = 0.2  # Toleransnivå för skillnad i avstånd

while True:
    # Hämta avstånd
    distance = sensor.raw_distance()

    # Om vi får ett avstånd (inte None), jämför och skriv ut
    if distance is not None:
        # Begränsa avståndet till 2 decimaler
        distance_rounded = round(distance, 1)

        # Om skillnaden mellan nuvarande och föregående avstånd är större än toleransen, skriv ut
        if previous_distance is None or abs(previous_distance - distance_rounded) > tolerance:
            print(f"Temperatur: {sensor.temperature} °C")
            print(f"Avstånd: {distance_rounded} cm")
            previous_distance = distance_rounded

    # Vänta --innan nästa mätning
    time.sleep(0.1)
