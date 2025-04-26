from flask import Flask, request
import RPi.GPIO as GPIO
import socket
import threading
import time

# Setup Flask
app = Flask(__name__)

# Define motor control pins
IN1, IN2, IN3, IN4 = 17, 18, 22, 23

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

motor_pins = [IN1, IN2, IN3, IN4]
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)

def stop():
    GPIO.output(IN1, 0)
    GPIO.output(IN2, 0)
    GPIO.output(IN3, 0)
    GPIO.output(IN4, 0)

def forward():
    GPIO.output(IN1, 1)
    GPIO.output(IN2, 0)
    GPIO.output(IN3, 1)
    GPIO.output(IN4, 0)

def backward():
    GPIO.output(IN1, 0)
    GPIO.output(IN2, 1)
    GPIO.output(IN3, 0)
    GPIO.output(IN4, 1)

def left():
    GPIO.output(IN1, 0)
    GPIO.output(IN2, 1)
    GPIO.output(IN3, 1)
    GPIO.output(IN4, 0)

def right():
    GPIO.output(IN1, 1)
    GPIO.output(IN2, 0)
    GPIO.output(IN3, 0)
    GPIO.output(IN4, 1)

# Handle GET requests from App
@app.route('/', methods=['GET'])
def control():
    state = request.args.get('State')
    if state == 'F':
        forward()
        return "Moving Forward"
    elif state == 'B':
        backward()
        return "Moving Backward"
    elif state == 'L':
        left()
        return "Turning Left"
    elif state == 'R':
        right()
        return "Turning Right"
    elif state == 'S':
        stop()
        return "Stopped"
    else:
        return "Invalid State", 400

# Display IP periodically in terminal
def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "Not connected"

def print_ip_continuously():
    while True:
        print(f"Current IP: {get_ip()}")
        time.sleep(10)

if __name__ == '__main__':
    threading.Thread(target=print_ip_continuously, daemon=True).start()
    print("Starting Robot Control Server...")
    print(f"Access the robot at http://{get_ip()}/")
    app.run(host='0.0.0.0', port=5000)
