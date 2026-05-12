# Ярошенко Георгій

import paho.mqtt.client as mqtt
import time
import random


class MQTTClient:
    def __init__(self, broker, port=1883):
        self.broker = broker
        self.port = port
        # Створюємо унікальний ID, щоб уникнути конфліктів на сервері
        client_id = f'python-mqtt-{random.randint(0, 1000)}'

        # Використовуємо актуальну версію API (v2)
        self.client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            client_id=client_id
        )

        # Налаштування callback-функцій
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_disconnect = self.on_disconnect

        self.is_connected = False

    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            self.is_connected = True
            print(f"Підключено до брокера: {self.broker}")
        else:
            print(f"Помилка підключення, код: {reason_code}")

    def on_publish(self, client, userdata, mid, reason_code, properties):
        print(f"Повідомлення успішно доставлено (mid={mid})")

    def on_disconnect(self, client, userdata, flags, reason_code, properties):
        self.is_connected = False
        print("Відключено від MQTT брокера")

    def connect(self):
        """Підключення до брокера з очікуванням статусу"""
        try:
            print(f"Спроба підключення до {self.broker}...")
            self.client.connect(self.broker, self.port, keepalive=60)
            self.client.loop_start()

            # Чекаємо до 5 секунд, поки прапорець is_connected стане True
            timeout = 5
            start_time = time.time()
            while not self.is_connected and (time.time() - start_time) < timeout:
                time.sleep(0.1)

            if not self.is_connected:
                print("Тайм-аут: не вдалося підключитися вчасно.")
        except Exception as e:
            print(f"Критична помилка: {e}")

    def publish(self, topic, message):
        """Публікація повідомлення"""
        if self.is_connected:
            result = self.client.publish(topic, message, qos=1)
            result.wait_for_publish()
            print(f"Опубліковано в тему '{topic}': {message}")
        else:
            print("Публікація неможлива: немає з'єднання.")

    def disconnect(self):
        """Коректне завершення роботи"""
        self.client.disconnect()
        self.client.loop_stop()


# Головний блок програми
if __name__ == "__main__":
    # Використовуємо стабільний публічний брокер
    # Якщо TimeoutError повториться, спробуйте роздати мобільний інтернет
    broker_url = "test.mosquitto.org"
    my_mqtt = MQTTClient(broker_url)

    my_mqtt.connect()

    if my_mqtt.is_connected:
        my_mqtt.publish("home/temperature/lab8", "24.5°C")
        time.sleep(1)  # Даємо час на завершення процесів
        my_mqtt.disconnect()
    else:
        print("Програма завершена через проблеми з мережею.")