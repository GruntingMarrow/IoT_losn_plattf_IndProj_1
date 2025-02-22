#samlingsprogram för att starta tilt och avståndsmätning

import subprocess
import time
import os
import signal

# Starta tilt-sensor programmet
tilt_process = subprocess.Popen(['python3', '/home/ulf/tilt.py'])

# Starta ultrasonic programmet
ultrasonic_process = subprocess.Popen(['python3', '/home/ulf/ultrasonic.py'])

time.sleep(2)

print("Tilt-sensor och Ultrasonic program startade.")

read_send_process = subprocess.Popen(["python3", "/home/ulf/read-send.py"])

time.sleep(1)

try:
    read_send_process.wait()
except KeyboardInterrupt:
    print("Avslutar processer...")
    tilt_process.terminate()
    ultrasonic_process.terminate()
    read_send_process.terminate()

# Lyssna på Ctrl+C (SIGINT) och andra avbrottssignaler
signal.signal(signal.SIGINT, cleanup_and_exit)
signal.signal(signal.SIGTERM, cleanup_and_exit)

# Vänta på att read-send.py avslutas
read_send_process.wait()

# Funktion för att stoppa programmen
#def stop_programs():
#    print("Stoppar programmen...")
#    tilt_process.terminate()
#    ultrasonic_process.terminate()
#    print("Programmen stoppade.")

# Vänta på att användaren trycker CTRL+C för att stänga av programmen
#try:
#    while True:
#        time.sleep(1)
#except KeyboardInterrupt:
#    stop_programs()

