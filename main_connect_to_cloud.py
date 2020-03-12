# Complete project details at https://RandomNerdTutorials.com

import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp

# from umqtt.robust import MQTTClient
# from umqtt.simple import MQTTClient


esp.osdebug(None)
import gc

gc.collect()

ssid = 'xfgjmxfgjmc'
password = 'weh87ryt665v6yc'
# mqtt_server = '192.168.77.142'
mqtt_server = 'air.creaxtive.com'
mqtt_port = 1883
mqtt_user = "pi"
mqtt_password = "woofa"
# EXAMPLE IP ADDRESS
# mqtt_server = '192.168.1.144'
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'10001001/warning'
# topic_sub = b'notification'
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


previous_connect_success = False

while True:
    if (time.time() - last_message) > message_interval:

        if previous_connect_success == False:
            try:
                print('now we connect again')
                client = MQTTClient(client_id, mqtt_server, port=mqtt_port, user=mqtt_user, password=mqtt_password)
                # client = MQTTClient(client_id, mqtt_server)
                client.set_callback(sub_cb)
                client.connect()
                client.subscribe(topic_sub)
                previous_connect_success = True


            except:
                previous_connect_success = False

        if previous_connect_success == True:
            try:
                client.check_msg()
                previous_connect_success = True
            except:
                print('cannot check message')

                previous_connect_success = False

        # if counter%8 == 0:
        #     previous_connect_success = False

        if previous_connect_success == False:
            try:

                client.disconnect()
                print('need to reconnect')
            except:
                pass

        last_message = time.time()
        print('counter', counter)
        counter += 1


