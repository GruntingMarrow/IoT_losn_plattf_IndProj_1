import subprocess
import time
import signal
import sys

# Starta tilt.py och ultrasonic.py
tilt_process = subprocess.Popen(['python3', '/home/ulf/tilt.py'])
ultrasonic_process = subprocess.Popen(['python3', '/home/ulf/ultrasonic.py'])

print("Tilt-sensor och Ultrasonic program startade.")

def cleanup_and_exit(signum, frame):
    """Avslutar alla processer vid avbrott (Ctrl+C eller SIGTERM)."""
    print("\nAvslutar processer...")
    tilt_process.terminate()
    ultrasonic_process.terminate()
    sys.exit(0)

# Lyssna på avbrottssignaler (Ctrl+C eller SIGTERM)
signal.signal(signal.SIGINT, cleanup_and_exit)
signal.signal(signal.SIGTERM, cleanup_and_exit)

# Håll programmet igång tills det avbryts
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    cleanup_and_exit(None, None)

