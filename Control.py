import RPi.GPIO as GPIO
import time
from datetime import datetime

# === CONFIGURATION ===
GPIO_PINS = [23, 24]          # Pins you want to control
ON_TIME  = "18:30"            # 6:30 PM
OFF_TIME = "23:59"            # 11:59 PM
# ======================

# Setup GPIO
GPIO.setmode(GPIO.BCM)
for pin in GPIO_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)   # Start OFF

def set_pins(state):
    """Set both pins HIGH or LOW"""
    value = GPIO.HIGH if state else GPIO.LOW
    for pin in GPIO_PINS:
        GPIO.output(pin, value)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] GPIO {GPIO_PINS} → {'ON' if state else 'OFF'}")

print("Daily GPIO controller started – waiting for scheduled times...")
print(f"Will turn ON  at {ON_TIME}, OFF at {OFF_TIME} every day")

try:
    while True:
        now = datetime.now().strftime("%H:%M")
        
        if now == ON_TIME:
            set_pins(True)
            time.sleep(65)        # Skip checking for ~1 minute to avoid double-trigger
        
        elif now == OFF_TIME:
            set_pins(False)
            time.sleep(65)
        
        else:
            # Sleep 20 seconds normally (very low CPU usage on Zero W)
            time.sleep(20)

except KeyboardInterrupt:
    print("\nShutting down...")
finally:
    GPIO.cleanup()
    print("GPIO cleaned up. Bye!")
