'''
referenced from spec example code
'''

import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connection returned result:", str(rc))

    client.subscribe("ece180d/test/use_the_ip_starting_with_169", qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected Disconnect")
    else:
        print("Expected Disconnect")

def on_message(client, userdata, message):
    print("Received message:", str(message.payload.decode()), "on topic", message.topic, "with QoS", str(message.qos))


if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    client.connect_async("mqtt.eclipseprojects.io")

    client.loop_start()

    while True:
        pass

    client.loop_stop()
    client.disconnect()