# Complete project details at https://RandomNerdTutorials.com

import time
# from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
from umqtt.robust import MQTTClient

esp.osdebug(None)
import gc

gc.collect()

ssid = 'xfgjmxfgjmc'
password = 'weh87ryt665v6yc'
mqtt_server = '192.168.77.142'
# mqtt_server = 'air.creaxtive.com'
mqtt_port = 1883
mqtt_user = "pi"
mqtt_password = "woofa"
# EXAMPLE IP ADDRESS
# mqtt_server = '192.168.1.144'
client_id = ubinascii.hexlify(machine.unique_id())
# topic_sub = b'10001001/warning'
topic_sub = b'notification'
topic_pub = b'hello'

last_message = 0
message_interval = 5
counter = 0

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
    pass

print('Connection successful')
print(station.ifconfig())


def sub_cb(topic, msg):
    print((topic, msg))


c = MQTTClient("umqtt_client", mqtt_server)
# Print diagnostic messages when retries/reconnects happens
c.DEBUG = True
c.set_callback(sub_cb)


if not c.connect(clean_session=False):

    c.subscribe(b"cc")
    print("New session being set up")

while 1:
    c.wait_msg()

c.disconnect()


