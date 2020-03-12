# Complete project details at https://RandomNerdTutorials.com

import time
# from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
# from umqtt.robust import MQTTClient
from umqtt.simple import MQTTClient
# from umqttsimple import MQTTClient

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
    if topic == b'notification' and msg == b'received':
        print('ESP received hello message')


print('check previous connection')
client = MQTTClient(client_id, mqtt_server)
client.set_callback(sub_cb)
client.connect()
client.subscribe(topic_sub)


previous_connect_success = False

while True:
    if (time.time() - last_message) > message_interval:

        # if previous_connect_success == False:
        #
        #
        #     print('check previous connection')
        #     client = MQTTClient(client_id, mqtt_server)
        #     client.set_callback(sub_cb)
        #     client.connect()
        #     client.subscribe(topic_sub)

        client.check_msg()
        # client.wait_msg()

        last_message = time.time()
        previous_connect_success = True


        #
        # try:
        #     client.check_msg()
        #     # client.wait_msg()
        #
        #
        #     last_message = time.time()
        #     previous_connect_success = True
        #
        # except:
        #     print('cannot check message')
        #     previous_connect_success = False



        counter += 1
        print('counter', counter)


