# Ярошенко Георгій

from abc import ABC, abstractmethod

# 2.1 Базовий клас для системи тарифікації
class Tariff(ABC):
    @abstractmethod
    def calculate_price(self, usage):
        pass

# Існуючі тарифи (Voice та Data)
class VoiceTariff(Tariff):
    def calculate_price(self, minutes):
        return minutes * 2.0  # Логіка для дзвінків

class DataTariff(Tariff):
    def calculate_price(self, megabytes):
        return megabytes * 0.1 # Логіка для інтернету

# 2.2 Розширення системи тарифом RoamingTariff
class RoamingTariff(Tariff):
    def calculate_price(self, minutes):
        return minutes * 15.0 # Новий тариф додано без зміни старого коду

# Перевірка виконання коду
if __name__ == "__main__":
    print("--- Завдання 2: OCP ---")
    voice = VoiceTariff()
    data = DataTariff()
    roaming = RoamingTariff()

    print(f"Вартість 10 хв розмови: {voice.calculate_price(10)} грн")
    print(f"Вартість 50 МБ інтернету: {data.calculate_price(50)} грн")
    print(f"Вартість 10 хв у роумінгу: {roaming.calculate_price(10)} грн")