import time
import json
import websocket
import random

# HOST = "ws://192.168.29.239:8082"
HOST = "ws://52.172.44.216:5000"

def sendData(timestamp='', sensorValues={}):
    data = {
        "deviceId": "IOT_DEVICE_2",
        "type": "IOT_DEVICE",
        "sensorData": {
            "deviceId": "IOT_DEVICE_2",
            "sensorType": "IOT_DEVICE",
            "timestamp": timestamp,
            "sensorValues": sensorValues,
        },
    }
    return json.dumps(data)

def main(ws):
    try:
        while True:
            #  Dummy temperature values
            amb_temp = round(random.uniform(20, 35), 2)   # ambient temp
            body_temp = round(random.uniform(36, 39), 2)  # body temp

            sensorValues = {
                "amb_temp": amb_temp,
                "body_temp": body_temp,
            }

            data = sendData(int(time.time() * 1000), sensorValues)

            ws.send(data)
            print("Sent:", data)  # debug

            time.sleep(1)

    except KeyboardInterrupt:
        pass

def on_message(ws, message):
    print("Received:", message)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws):
    print("\nConnection Closed\n")

def on_open(ws):
    print("Connected!")
    main(ws)

if __name__ == "__main__":
    try:
        print(f"Connecting to Server at {HOST}...")

        ws = websocket.WebSocketApp(
            HOST,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )

        ws.on_open = on_open
        ws.run_forever()

    except Exception as e:
        print(e)
        print("Retrying in 10 seconds...")
        time.sleep(10)