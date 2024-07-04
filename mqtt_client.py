import json
import os

from paho.mqtt import client as mqtt

broker = os.environ['MQTT_HOST']
port = 1883
client_id = 'python-mqtt-hcyun'
username = 'mqtt'
password = 'mqtt'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)


    # For paho-mqtt 2.0.0, you need to set callback_api_version.
    client = mqtt.Client(client_id=client_id, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client, data, topic):
    result = client.publish(topic, json.dumps(data))
    status = result[0]
    if status == 0:
        print(f"Send {data} to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")


def run(data, topic):
    client = connect_mqtt()
    client.loop_start()
    publish(client, data, topic)
    client.loop_stop()

