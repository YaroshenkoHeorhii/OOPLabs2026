# Ярошенко Георгій

from abc import ABC, abstractmethod

class NetworkConnection(ABC):
    @abstractmethod
    def connect(self):
        pass

# 3.1 Реалізація взаємозамінних підкласів
class LTEConnection(NetworkConnection):
    def connect(self):
        print("Підключено до LTE")

class WiFiConnection(NetworkConnection):
    def connect(self):
        print("Підключено до WiFi")

# 3.2 Виправлена ієрархія для SatelliteConnection
class SatelliteConnection(NetworkConnection):
    def _calibrate_dish(self):
        # Специфічна логіка прихована від клієнта
        print("Калібрування антени...")

    def connect(self):
        # Базовий метод відпрацьовує очікувано
        self._calibrate_dish()
        print("Супутниковий зв'язок встановлено")

# Перевірка виконання коду
if __name__ == "__main__":
    print("--- Завдання 3: LSP ---")
    # Демонстрація взаємозамінності
    connections = [LTEConnection(), WiFiConnection(), SatelliteConnection()]

    for conn in connections:
        conn.connect()