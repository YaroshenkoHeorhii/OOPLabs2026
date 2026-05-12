# Ярошенко Георгій

import unittest
from unittest.mock import Mock
from parameterized import parameterized


# --- 1. Клас MathTool (Завдання 1) ---
class MathTool:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Division by zero")
        return a / b


# --- 2. Клас LibraryItem (Завдання 2) ---
class LibraryItem:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def details(self):
        return f"{self.title} by {self.author} ({self.year})"


# --- 3. Класи для Mock (Завдання 3) ---
class NotificationService:
    def send(self, message):
        pass


class UserManager:
    def __init__(self, service):
        self.service = service

    def notify_user(self, message):
        self.service.send(message)


# --- 4. Функція для параметризації (Завдання 4) ---
def check_even(number):
    return number % 2 == 0


# --- ТЕСТИ ---
class TestLaboratoryWork(unittest.TestCase):

    def setUp(self):
        self.math = MathTool()

    def test_math_tool(self):
        self.assertEqual(self.math.add(10, 5), 15)
        self.assertEqual(self.math.subtract(10, 5), 5)
        self.assertEqual(self.math.multiply(10, 5), 50)
        self.assertEqual(self.math.divide(10, 5), 2)

        # Перевірка виключення при діленні на нуль
        with self.assertRaises(ValueError):
            self.math.divide(10, 0)

    def test_library_item_details(self):
        item = LibraryItem("Kobzar", "Taras Shevchenko", 1840)
        self.assertEqual(item.details(), "Kobzar by Taras Shevchenko (1840)")

    def test_user_manager_mock(self):
        # Створюємо мок-об'єкт замість реального сервісу
        mock_service = Mock(spec=NotificationService)
        manager = UserManager(mock_service)

        manager.notify_user("Hello!")

        # Перевіряємо, чи був викликаний метод send з правильним параметром
        mock_service.send.assert_called_once_with("Hello!")

    # Параметризований тест
    @parameterized.expand([
        ("even_pos", 2, True),
        ("odd_pos", 3, False),
        ("zero", 0, True),
        ("even_neg", -4, True),
    ])
    def test_check_even_parameterized(self, name, val, expected):
        self.assertEqual(check_even(val), expected)


if __name__ == "__main__":
    unittest.main()