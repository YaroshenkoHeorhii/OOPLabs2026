# Ярошенко Георгій

# 1.1 Розділення класу CallReport
class CallReportGenerator:
    # Формує звіт про дзвінки
    def generate(self, calls_data):
        return "Звіт згенеровано"

class CallReportSaver:
    # Зберігає готові дані у файл
    def save(self, report, filename):
        print(f"Звіт збережено у {filename}")

# 1.2 Розділення класу Subscriber
class SubscriberData:
    # Зберігає виключно дані абонента
    def __init__(self, phone_number):
        self.phone_number = phone_number

class SmsSender:
    # Відповідає за відправку SMS
    def send(self, subscriber_data, message):
        print(f"Повідомлення на {subscriber_data.phone_number}: {message}")

class BalanceCalculator:
    # Розраховує баланс окремо від інших процесів
    def calculate(self, subscriber_data):
        return 150.0

# Перевірка завдання
if __name__ == "__main__":
    print("--- Завдання 1.1: Call Report ---")
    report_gen = CallReportGenerator()
    report_saver = CallReportSaver()

    report_content = report_gen.generate("дані_дзвінків_за_місяць")
    print(report_content)
    report_saver.save(report_content, "call_report_01.txt")

    print("\n--- Завдання 1.2: Subscriber ---")
    subscriber = SubscriberData("+380991234567")

    sms = SmsSender()
    sms.send(subscriber, "Вітаємо у нашій мережі!")

    calc = BalanceCalculator()
    balance = calc.calculate(subscriber)
    print(f"Поточний баланс: {balance} грн")