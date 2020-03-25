#
# Modules
#

import streams

from riverdi.displays.bt81x import ctp50
from bridgetek.bt81x import bt81x

from wireless import wifi
from espressif.esp32net import esp32wifi as wifi_driver

from okdo.iot import iot
from okdo.iot import mqtt_client

#
# Variables
#

RLOGO_W = 304
RLOGO_H = 124
WIFI_SSID = "..."
WIFI_PASS = "..."
DEV_ID = "..."
DEV_TOKEN = "..."

cpu_temp = 0
cpu_load = 0
last_temp = 0
last_load = 0

#
# Functions
#

def connectToLocalNetwork():
    wifi_driver.auto_init()
    try:
        wifi.link(WIFI_SSID, wifi.WIFI_WPA2, WIFI_PASS)
    except Exception as e:
        print("Can't connect to WiFi - Check network name and password", e)
        while True:
            sleep(1000)

def printNetworkParametes():
    networkInfo = wifi.link_info()
    print("IP: ", networkInfo[0]);
    print("Netmask: ", networkInfo[1]);
    print("Gateway: ", networkInfo[2]);
    print("DNS: ", networkInfo[3]);

def displaySpinner(operation, info):
    bt81x.dl_start()
    bt81x.clear(1, 1, 1)
    txt_oper = bt81x.Text(400, 260, 24, bt81x.OPT_CENTERX | bt81x.OPT_CENTERY,
                        operation, )
    txt_info = bt81x.Text(400, 300, 24, bt81x.OPT_CENTERX | bt81x.OPT_CENTERY,
                        info, )
    bt81x.add_text(txt_oper)
    bt81x.add_text(txt_info)
    bt81x.spinner(400, 160, bt81x. SPINNER_LINE, 0)
    bt81x.display()
    bt81x.swap_and_empty()

def displayUpdate():
    
    global cpu_temp
    global cpu_load

    image_1 = bt81x.Bitmap(1, 0,
                (bt81x.ARGB4, RLOGO_W * 2),
                (bt81x.BILINEAR, bt81x.BORDER, bt81x.BORDER,
                    RLOGO_W, RLOGO_H))
    bt81x.dl_start()
    bt81x.load_image(0, 0, 'rlogo.png')
    bt81x.clear(1, 1, 1)
    bt81x.set_background(255,255,255)
    image_1.prepare_draw()
    image_1.draw((248, 35), vertex_fmt=0)
    txt_temp = bt81x.Text(500, 260, 31, bt81x.OPT_RIGHTX | bt81x.OPT_CENTERY,"Temperature : %2.1f" % cpu_temp, )
    txt_load = bt81x.Text(500, 320, 31, bt81x.OPT_RIGHTX | bt81x.OPT_CENTERY,"Load : %2.1f" % cpu_load, )
    bt81x.add_text(txt_temp)
    bt81x.add_text(txt_load)
    bt81x.display()
    bt81x.swap_and_empty()

def temp_cb(asset, value, previous_value):
    global cpu_temp
    if (asset == 'cpu_temperature'):
        print("CPU temperature:", value)
        cpu_temp = value
    else:
        print("Something is wrong")

def load_cb(asset, value, previous_value):
    global cpu_load
    if (asset == 'cpu_load'):
        print("CPU load:", value)
        cpu_load = value
    else:
        print("Something is wrong")

#
# Program
#

new_resource('rlogo.png')
streams.serial()
bt81x.init(SPI0, D4, D33, D34)
connectToLocalNetwork()
displaySpinner("Connecting to WiFI Network", WIFI_SSID)
sleep(2000)
printNetworkParametes()

device = iot.Device(DEV_ID,DEV_TOKEN,mqtt_client.MqttClient)
device.connect()
device.watch_command("cpu_temperature", temp_cb)
device.watch_command("cpu_load", load_cb)
device.run()
displaySpinner("Connecting to OKdo", "")

while True:   
    if (last_temp != cpu_temp) or (last_load != cpu_load):
        displayUpdate()
        last_load = cpu_load
        last_temp = cpu_temp
    sleep(200)
