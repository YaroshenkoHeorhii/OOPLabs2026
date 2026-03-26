# Ярошенко Георгій

from abc import ABC, abstractmethod

# 4.1 Розділення універсального інтерфейсу
class ICallable(ABC):
    @abstractmethod
    def make_call(self): pass

class ISmsSender(ABC):
    @abstractmethod
    def send_sms(self): pass

class INetworkConnectable(ABC):
    @abstractmethod
    def connect_to_network(self): pass

# Смартфон реалізує всі необхідні йому можливості
class Smartphone(ICallable, ISmsSender, INetworkConnectable):
    def make_call(self): print("Дзвінок...")
    def send_sms(self): print("Відправка SMS...")
    def connect_to_network(self): print("Підключення до мережі...")

# 4.2 IoT-пристрій імплементує лише передачу даних
class IoTDevice(INetworkConnectable):
    def connect_to_network(self):
        print("Передача даних з датчика у мережу")

# Перевірка виконання коду
if __name__ == "__main__":
    print("--- Завдання 4: ISP ---")
    phone = Smartphone()
    print("Робота смартфона:")
    phone.make_call()
    phone.send_sms()
    phone.connect_to_network()

    sensor = IoTDevice()
    print("\nРобота IoT-датчика:")
    # Датчик має доступ лише до передачі даних
    sensor.connect_to_network()