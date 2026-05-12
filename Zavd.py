# Ярошенко Георгій

import requests

class RestClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint):
        """Виконує HTTP GET-запит та повертає дані."""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Помилка GET: Статус {response.status_code}")
                return None
        except Exception as e:
            print(f"Виникла помилка: {e}")
            return None

    def post(self, endpoint, data):
        """Виконує HTTP POST-запит з переданими даними."""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.post(url, json=data)
            if response.status_code == 201:
                return response.json()
            else:
                print(f"Помилка POST: Статус {response.status_code}")
                return None
        except Exception as e:
            print(f"Виникла помилка: {e}")
            return None

# Демонстрація роботи
if __name__ == "__main__":
    client = RestClient("https://jsonplaceholder.typicode.com")

    # 1. Приклад GET-запиту (отримання списку користувачів)
    print("--- Отримання даних (GET) ---")
    users = client.get("users")
    if users:
        print(f"Отримано користувачів: {len(users)}")
        print(f"Перший користувач: {users[0]['name']}")

    # 2. Приклад POST-запиту (створення нового посту)
    print("\n--- Створення запису (POST) ---")
    new_post = {
        "title": "ООП Лабораторна",
        "body": "Реалізація клієнта завершена успішно.",
        "userId": 1
    }
    created_post = client.post("posts", new_post)
    if created_post:
        print(f"Сервер підтвердив створення: {created_post}")