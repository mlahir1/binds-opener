import RPi.GPIO as GPIO
import time
import sys

args = sys.argv[1:]
# Pin Definitions
PIN1 = 23  # GPIO3
PIN2 = 22  # GPIO4
DELAY = int(args[1])  # 2.5 minutes 
INPUT_PIN_BOT = 17 

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN1, GPIO.OUT)
GPIO.setup(PIN2, GPIO.OUT)
GPIO.setup(INPUT_PIN_BOT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Initialize both pins LOW
GPIO.output(PIN1, GPIO.LOW)
GPIO.output(PIN2, GPIO.LOW)

print("Toggling GPIO3 and GPIO4 every 2 minutes. Press Ctrl+C to stop.")
print(f"Monitoring GPIO {INPUT_PIN_BOT}")
try:
    # if args[0].lower() == "routine":
    #     # Toggle pins
    #     GPIO.output(PIN1, GPIO.LOW)
    #     GPIO.output(PIN2, GPIO.HIGH)
    #     # Print current state for debugging
    #     print(f"GPIO3: {'ON' if GPIO.input(PIN1) else 'OFF'}, GPIO4: {'ON' if GPIO.input(PIN2) else 'OFF'}")
    #     # Wait 2 minutes
    #     time.sleep(DELAY)
    #     GPIO.output(PIN1, GPIO.HIGH)
    #     GPIO.output(PIN2, GPIO.LOW)
    #     print(f"GPIO3: {'ON' if GPIO.input(PIN1) else 'OFF'}, GPIO4: {'ON' if GPIO.input(PIN2) else 'OFF'}")
    #     time.sleep(DELAY)
    if args[0].lower() == "down" or args[0].lower() == "reset":
        GPIO.output(PIN1, GPIO.LOW)
        GPIO.output(PIN2, GPIO.HIGH)
        print(f"GPIO3: {'ON' if GPIO.input(PIN1) else 'OFF'}, GPIO4: {'ON' if GPIO.input(PIN2) else 'OFF'}")
        rbot_flag = GPIO.input(INPUT_PIN_BOT)
        print(rbot_flag)
        for i in range(DELAY+20): # 2.52.5 min delays
            if rbot_flag:
                print("Reached Bottom")
                break
            time.sleep(1)
            rbot_flag = GPIO.input(INPUT_PIN_BOT)
    if args[0].lower() == "up" or args[0].lower() == "reset":
        GPIO.output(PIN1, GPIO.HIGH)
        GPIO.output(PIN2, GPIO.LOW)
        print(f"GPIO3: {'ON' if GPIO.input(PIN1) else 'OFF'}, GPIO4: {'ON' if GPIO.input(PIN2) else 'OFF'}")
        time.sleep(DELAY)
    GPIO.output(PIN1, GPIO.LOW)
    GPIO.output(PIN2, GPIO.LOW)
except KeyboardInterrupt:
    print("\nStopping program and cleaning up GPIO.")
    GPIO.output(PIN1, GPIO.LOW)
    GPIO.output(PIN2, GPIO.LOW)
    print(f"GPIO3: {'ON' if GPIO.input(PIN1) else 'OFF'}, GPIO4: {'ON' if GPIO.input(PIN2) else 'OFF'}")
    GPIO.cleanup()
