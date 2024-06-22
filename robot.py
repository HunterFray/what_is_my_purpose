from time import sleep
from machine import Pin, ADC, PWM
from motor_driver import motor_driver
import time
import network
import socket
import secrets

#Setting up WiFi connection
ssid = secrets.ssid
password = secrets.password

#start up webserver


#Setting up the potentiometers
pot1 = ADC(Pin(27 ))
pot1reading = 0
pot2 = ADC(Pin(26))
pot2reading = 0

#setting up the PWM for servo's
servo1 = PWM(Pin(2))
servo1.freq(50)
servo2 = PWM(Pin(3))
servo2.freq(50)

#setting up the motor driver

motor = motor_driver(5,6,7,8) #Set pins for motor A and B  M1A=Pin0,M1B=Pin1,M2A=Pin3,M2B=Pin4

#setting up the laser pointer
laser = Pin(28, Pin.OUT)

#PWM min and max value
in_min = 0
in_max = 65535
#servo motor min and max degrees
out_min = 1000
out_max = 9000
########################################################
#                     FUNCTIONS                        #
########################################################

# Motor Control Functions
def forward():
    motor.speed(100,100)

def back():
    motor.speed(-50,-50)
    
def left():
    motor.speed(-50,50)
    
def right():
    motor.speed(50,-50)
def stop():
    motor.speed(0,0)
    
def laser_on():
    laser.value(1)

def laser_off():
    laser.value(0)
    
def wifi_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print("Waiting on wifi connection")
        time.sleep(1)
    ip = wlan.ifconfig()[0]
    print(wlan.ifconfig())
    return ip
    
def webpage():
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <title>Robot Control</title>
            </head>
            <center><b>
            <form action="./forward">
            <input type="submit" value="Forward" style="height:120px; width:120px" />
            </form>
            <table><tr>
            <td><form action="./left">
            <input type="submit" value="Left" style="height:120px; width:120px" />
            </form></td>
            <td><form action="./stop">
            <input type="submit" value="Stop" style="height:120px; width:120px" />
            </form></td>
            <td><form action="./right">
            <input type="submit" value="Right" style="height:120px; width:120px" />
            </form></td>
            </tr></table>
            <form action="./back">
            <input type="submit" value="Back" style="height:120px; width:120px" />
            </form>
            <form action="./laser_on">
            <input type="submit" value="laser on">
            </form>
            <form action="./laser_off">
            <input type="submit" value="laser off">
            </form>
            </body>
            </html>
            """
    return str(html)

def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def serve(connection):
    #Start web server
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/forward?':
            forward()
        elif request =='/left?':
              left()
        elif request =='/stop?':
              stop()
        elif request =='/right?':
              right()
        elif request =='/back?':
              back()
        elif request =='/laser_on?':
              laser_on()
        elif request =='/laser_off?':
              laser_off()
        html = webpage()
        client.send(html)
        client.close()
#######################################################
#                  Main Program                       #
#######################################################
#initiate WiFi Connection

while True:
    try:
        ip = wifi_connect()
        connection = open_socket(ip)
        serve(connection)
    except KeyboardInterrupt:
        machine.reset()
    #laser.value(1)
    pot1value = pot1.read_u16()
    print(pot1value)
    Servo1 = (pot1value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    servo1.duty_u16(int(Servo1))
    pot2value = pot2.read_u16()
    print(pot2value)
    Servo2 = (pot2value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    servo2.duty_u16(int(Servo2))
    
                                                                                        