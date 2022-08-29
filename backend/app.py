import time
import datetime
from datetime import datetime
from RPi import GPIO
import threading
from flask_cors import CORS
from flask_socketio import SocketIO
from flask import Flask, jsonify, request 
from repositories.DataRepository import DataRepository
from selenium import webdriver
import spidev
from board import SCL, SDA
import busio
from oled_text import OledText
from oled_text import OledText
import serial

sensor_file_name = '/sys/bus/w1/devices/28-012022646039/w1_slave'
ph_sens = 0

temps=[]
def time_now():
    now = datetime.datetime.now()
    print("datetime:", now)
    
def setup_gpio():
    global spi, oled, disp 
    spi = spidev.SpiDev()
    spi.open(0,0)
    spi.max_speed_hz = 10 ** 5
    # disp = lcd()
    # disp.lcd_clear()
    # disp.backlight(0)
    # disp.lcd_display_string("test")
    setupSerial()

def setupSerial():
    global ser
    ser = serial.Serial('/dev/serial0')
    ser.reset_input_buffer()
    time.sleep(2)


i2c = busio.I2C(SCL, SDA)
# Create the display, pass its pixel dimensions
oled = OledText(i2c, 128, 64)
# Write to the oled
# oled.layout = Layout64.layout_3medium_3icons()

def read_spi(channel):
    global spi
    spidata = spi.xfer2([1,(8|channel)<<4,0])
    return ((spidata[1] & 3) << 8) | spidata[2]


def temp_sens():
    sensor_file = open(sensor_file_name, 'r')
    for line in sensor_file:
        if line.find("t=") >= 0:
            temp = float(line[line.find("t=")+2:]) / 1000
            # if temp == True:
            sensor_file.close        
            return temp

def read_serialport():
    string_ascii = ser.readline()
    string_utf = string_ascii.decode(encoding='utf-8').strip("\n")
    return(f"{string_utf}")

#volg deviceid waarde datum
def read_ldr(): #works
    global oled
    upm = DataRepository.read_device_onderwerp("light")
    print(upm)
    # print("oegaboega")
    ldr_waarde = read_spi(0)
    DataRepository.update_meting(upm["deviceid"], ldr_waarde, datetime.now())
    socketio.emit('B2F_meting_ldr', {'waarde': ldr_waarde}, broadcast=True)
    print(id)
    oled.text(ldr_waarde, 2)  # Line 2
    time.sleep(1)

def read_temp(): #works
    global oled
    upm = DataRepository.read_device_onderwerp("temperature")
    print(upm)
    # print("stonks")  
    temp_waarde = temp_sens()
    DataRepository.update_meting(upm["deviceid"], temp_waarde, datetime.now())
    socketio.emit('B2F_temp_sens', {'waarde': temp_waarde}, broadcast=True)
    print(id)
    oled.text(temp_waarde, 1)  # Line 1
    time.sleep(1)

def read_ph():
    upm = DataRepository.read_device_onderwerp("acidity")
    print(upm)
    # print("moooooooooo")
    ph_waarde = read_serialport()
    DataRepository.update_meting(upm["deviceid"], ph_waarde, datetime.now())
    socketio.emit('B2F_ph_sens', {'waarde': ph_waarde}, broadcast=True)
    print(id)
    oled.text(ph_waarde, 3)  # Line 3
    time.sleep(1)


# Code for flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=False,
                    engineio_logger=False, ping_timeout=1)
CORS(app)

@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print(e)

# Custom endpoint
endpoint ="/api/v1"

# API ENDPOINTS

@app.route('/')
def index():
    return "please go to API path", 403

@app.route(endpoint + '/temp', methods=['GET'])
def get_history_temp():
    if request.method == 'GET':
        temps = DataRepository.read_history_temp()
        return jsonify(temps), 200


@socketio.on('connect')# Send to the client!
def initial_connection():
    print('A new client connect') 
    read_ldr()
    read_temp()
     # vraag de status op van de lampen uit de DB
    # status = DataRepository.read_status_lampen()
    # status = DataRepository.read_device_onderwerp()
    # emit('status_device', {'device': status}, broadcast=True)     

# START een thread op. Belangrijk!!! Debugging moet UIT staan op start van de server, anders start de thread dubbel op
# werk enkel met de packages gevent en gevent-websocket.
def all_out():
    while True:
        print('*** We zetten alles uit **')
        read_ldr()
        read_temp()
        read_ph()
        # read_spi()
        # temp_sens()

def start_thread():
    print("**** Starting THREAD ****")
    thread = threading.Thread(target=all_out, args=(), daemon=True)
    thread.start()

def move_screen(self): #lcd longer than 16bit
    self.send_instruction(0b00011000)

def start_chrome_kiosk(): #screen to rpi --> opening website
    import os
    os.environ['DISPLAY'] = ':0.0'
    options = webdriver.ChromeOptions()
    # options.headless = True
    # options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    # options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    # options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--kiosk')
    # chrome_options.add_argument('--no-sandbox')         
    # options.add_argument("disable-infobars")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)
    driver.get("http://localhost")
    while True:
        pass

def start_chrome_thread():
    print("**** Starting CHROME ****")
    chromeThread = threading.Thread(target=start_chrome_kiosk, args=(), daemon=True)
    chromeThread.start()


if __name__ == '__main__':
    try:
        setup_gpio()
        start_thread()
        # read_ldr()
        # read_temp()
        start_chrome_thread()
        print("**** Starting APP ****")
        socketio.run(app, debug=False, host='0.0.0.0')
    except KeyboardInterrupt:
        print ('KeyboardInterrupt exception is caught')
    finally:
        GPIO.cleanup()



# @app.route(endpoint + "/sensor", methods=["GET", "POST"])
# def sensor():
#     if request.method =="GET":
#         data = DataRepository.read_status_deviceid()
#         if data is not None:
#             return jsonify(deviceid=data), 200
#         else:
#             return jsonify(message="error"), 404
#     elif request.method == "POST":
#         gegevens = DataRepository.json_or_formdata(request)
#         print(gegevens)
#         data = DataRepository.create_device(gegevens["onderwerp"], gegevens["meetapparaat"], gegevens["deviceid"], gegevens["meeteenheid"], gegevens["beschrijving"])
#         return jsonify(deviceid = data), 201


# def ldr():    
#     spi = spidev.SpiDev()
#     spi.open(0,0)
#     spi.max_speed_hz = 10 ** 5
    
#     def read_spi(channel):
#         spidata = spi.xfer2([1,(8|channel)<<4,0])
#         return ((spidata[1] & 3) << 8) | spidata[2]
    
#     try:
#         while True:
#             channeldata = read_spi(0)
#             print("Waarde = {}".format(channeldata))
#             time.sleep(1)
    
#     except KeyboardInterrupt:
#         spi.close()

# @socketio.on("xxxxxxxxxxxxxxxxxxxxxxxx")
# def xxxxxxxxxxxxxxxxxxxxxxxx(data):
#     #getting data 
#     device_id = data['deviceid']
#     onderwerp = data['onderwerp']
#     print(f"{device_id} geeft {onderwerp}")

#     #stel de status in op de DB
#     res = DataRepository.update_meting(device_id)



# def write_serialport(time):
#     string_utf = str(time)
#     string_ascii = string_utf.encode(encoding='utf-8')
#     print(string_ascii)
#     ser.write(string_ascii)