# Ярошенко Георгій

from abc import ABC, abstractmethod

# 5.1 Абстракція логера
class Logger(ABC):
    @abstractmethod
    def log(self, message): pass

# 5.2 Варіанти підключення логерів
class FileLogger(Logger):
    def log(self, message):
        print(f"Запис у файл: {message}")

class ServerLogger(Logger):
    def log(self, message):
        print(f"Відправка на сервер: {message}")

class ConsoleLogger(Logger):
    def log(self, message):
        print(f"Вивід у консоль: {message}")

# Клас моніторингу не потребує змін при зміні логера
class NetworkMonitor:
    def __init__(self, logger: Logger):
        self.logger = logger  # Залежність інжектована через конструктор

    def check(self):
        self.logger.log("успіх")

# Перевірка коду
if __name__ == "__main__":
    print("--- Завдання 5: DIP ---")

    # Монітор з логуванням у файл
    file_monitor = NetworkMonitor(FileLogger())
    file_monitor.check()

    # Монітор з логуванням на сервер
    server_monitor = NetworkMonitor(ServerLogger())
    server_monitor.check()

    # Монітор з виводом у консоль
    console_monitor = NetworkMonitor(ConsoleLogger())
    console_monitor.check()