import time
import json
import random
import paho.mqtt.client as mqtt

# ==== REQUIRED BY ASSIGNMENT ====
student_name = "Pyla Mohan Sai"
unique_id = "42130367"   # <-- put your register number
topic = "home/pylamohan-2025/sensor"
# =================================

BROKER_IP = "10.43.29.159"   # IP of your Home Assistant VM
BROKER_PORT = 1883
MQTT_USERNAME = "pyla"
MQTT_PASSWORD = "mohansai12345"

connected = False  # global flag


def on_connect(client, userdata, flags, rc, *extra):
    global connected
    if rc == 0:
        connected = True
        print("MQTT connection established (rc=0)")
    else:
        print(f"MQTT connection failed, rc={rc}")


def main():
    global connected

    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect

    client.loop_start()
    client.connect(BROKER_IP, BROKER_PORT, 60)

    print("Connecting to MQTT broker...")
    timeout = time.time() + 10
    while not connected and time.time() < timeout:
        time.sleep(0.1)

    if not connected:
        print("Could not establish MQTT connection within 10 seconds.")
        client.loop_stop()
        client.disconnect()
        return

    print("Connected to MQTT broker, starting publish loop...")

    try:
        while True:
            temperature = 25
            humidity = 60
            light = random.randint(100, 400)

            payload = {
                "temperature": temperature,
                "humidity": humidity,
                "light": light
            }

            payload_str = json.dumps(payload)
            result = client.publish(topic, payload_str)

            print(f"Published to {topic}: {payload_str}, result={result.rc}")

            time.sleep(5)

    except KeyboardInterrupt:
        print("Stopping publisher...")

    finally:
        client.loop_stop()
        client.disconnect()
        print("Disconnected from MQTT broker")


if __name__ == "__main__":
    main()
