#samlingsprogram för att starta tilt och avståndsmätning

import subprocess
import time
import os
import signal

# Starta tilt-sensor programmet
tilt_process = subprocess.Popen(['python3', '/home/ulf/tilt.py'])

# Starta ultrasonic programmet
ultrasonic_process = subprocess.Popen(['python3', '/home/ulf/ultrasonic.py'])

print("Tilt-sensor och Ultrasonic program startade.")

# Funktion för att stoppa programmen
def stop_programs():
    print("Stoppar programmen...")
    tilt_process.terminate()
    ultrasonic_process.terminate()
    print("Programmen stoppade.")

# Vänta på att användaren trycker CTRL+C för att stänga av programmen
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    stop_programs()

