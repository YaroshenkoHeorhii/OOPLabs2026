# Ярошенко Георгій

import sqlite3
import pandas as pd
import re


class DataPreparation:
    """Клас для завантаження, очищення даних та їх експорту в SQLite."""

    def __init__(self, db_name, csv_file):
        self.db_name = db_name
        self.csv_file = csv_file
        self.conn = sqlite3.connect(self.db_name)
        self.df = None

    def load_and_clean_data(self):
        # 1. Завантаження даних
        self.df = pd.read_csv(self.csv_file)
        self.df.columns = self.df.columns.str.strip()

        # Функції для вилучення числових значень зарплат
        def extract_salaries(text):
            nums = re.findall(r'\d+', str(text).replace(',', ''))
            if not nums: return pd.Series([0, 0, 0])
            if len(nums) >= 2:
                return pd.Series([int(nums[0]), int(nums[-1]), (int(nums[0]) + int(nums[-1])) / 2])
            return pd.Series([int(nums[0]), int(nums[0]), int(nums[0])])

        # Створення нових числових колонок для SQL
        self.df[['Min_Salary', 'Max_Salary', 'Avg_Salary']] = self.df['Salary Range'].apply(extract_salaries)

        # Перетворення дати та витягнення року
        self.df['Date Posted'] = pd.to_datetime(self.df['Date Posted'])
        self.df['Year'] = self.df['Date Posted'].dt.year

    def save_to_sqlite(self, table_name='jobs'):
        # 4. Завантаження даних у базу SQLite
        self.df.to_sql(table_name, self.conn, if_exists='replace', index=False)
        print(f"Дані успішно завантажено в таблицю '{table_name}'.\n")

    def get_connection(self):
        return self.conn


class BasicQueries:
    """Клас для Завдання 2: Основні запити SQL."""

    def __init__(self, conn):
        self.conn = conn

    def run(self):
        print("--- Завдання 2. Основні запити SQL ---")

        # 1. Перші 10 вакансій
        q1 = "SELECT * FROM jobs LIMIT 10;"
        print("\n1. Перші 10 вакансій:")
        print(pd.read_sql(q1, self.conn)[['Job Title', 'Company']].head())

        # 2. Вакансії з вимогою SQL
        q2 = "SELECT * FROM jobs WHERE \"Required Skills\" LIKE '%SQL%';"
        print("\n2. Вакансії, що вимагають SQL (перші 5):")
        print(pd.read_sql(q2, self.conn)[['Job Title', 'Required Skills']].head())

        # 3. Унікальні Location та Company
        q3 = "SELECT DISTINCT Location, Company FROM jobs LIMIT 5;"
        print("\n3. Унікальні локації та компанії (зразок):")
        print(pd.read_sql(q3, self.conn))


class AnalyticalQueries:
    """Клас для Завдань 3 та 4: Аналітичні запити та агрегатні функції."""

    def __init__(self, conn):
        self.conn = conn

    def run(self):
        print("\n--- Завдання 3 та 4. Аналітичні запити ---")

        # Середня зарплата за рівнем досвіду
        q1 = "SELECT \"Experience Level\", AVG(Avg_Salary) as Average_Salary FROM jobs GROUP BY \"Experience Level\";"
        print("\nСередня зарплата за рівнем досвіду:")
        print(pd.read_sql(q1, self.conn))

        # Кількість вакансій за рівнем досвіду
        q2 = "SELECT \"Experience Level\", COUNT(*) as Job_Count FROM jobs GROUP BY \"Experience Level\";"
        print("\nКількість вакансій за рівнем досвіду:")
        print(pd.read_sql(q2, self.conn))

        # Мінімальна та максимальна зарплата серед усіх
        q3 = "SELECT MIN(Min_Salary) as Absolute_Min, MAX(Max_Salary) as Absolute_Max FROM jobs;"
        print("\nМінімальна та максимальна зарплата загалом:")
        print(pd.read_sql(q3, self.conn))

        # Кількість вакансій за індустрією (зарплата > 50,000)
        q4 = "SELECT Industry, COUNT(*) as Job_Count FROM jobs WHERE Avg_Salary > 50000 GROUP BY Industry ORDER BY Job_Count DESC LIMIT 5;"
        print("\nВакансії в індустріях із зарплатою > 50k (Топ 5):")
        print(pd.read_sql(q4, self.conn))


class ComplexQueries:
    """Клас для Завдань 5 та 6: Складні та додаткові запити."""

    def __init__(self, conn, df):
        self.conn = conn
        self.df = df  # Pandas DataFrame передається для завдання зі сплітом навичок

    def run(self):
        print("\n--- Завдання 5. Складні запити ---")

        # Загальна кількість вакансій в індустрії за типом роботи
        q1 = "SELECT Industry, \"Job Type\", COUNT(*) as Job_Count FROM jobs GROUP BY Industry, \"Job Type\" LIMIT 5;"
        print("\nВакансії за індустрією та типом (фрагмент):")
        print(pd.read_sql(q1, self.conn))

        # Середня зарплата за локацією та рівнем досвіду
        q2 = "SELECT Location, \"Experience Level\", AVG(Avg_Salary) as Average_Salary FROM jobs GROUP BY Location, \"Experience Level\" LIMIT 5;"
        print("\nСередня зарплата за локацією та досвідом (фрагмент):")
        print(pd.read_sql(q2, self.conn))

        print("\n--- Завдання 6. Додаткові запити ---")

        # 5 вакансій з найвищою верхньою межею зарплати
        q3 = "SELECT \"Job Title\", Company, Max_Salary FROM jobs ORDER BY Max_Salary DESC LIMIT 5;"
        print("\nТоп 5 вакансій за максимальною зарплатою:")
        print(pd.read_sql(q3, self.conn))

        # Компанії з найбільшою кількістю вакансій у 2023 році
        q4 = "SELECT Company, COUNT(*) as Job_Count FROM jobs WHERE Year = 2023 GROUP BY Company ORDER BY Job_Count DESC LIMIT 5;"
        print("\nТоп компаній за кількістю вакансій у 2023 році:")
        print(pd.read_sql(q4, self.conn))

        # Підрахунок навичок (за допомогою Pandas, оскільки в SQLite немає вбудованого split)
        print("\nНайбільш затребувані навички (розділені комою):")
        all_skills = self.df['Required Skills'].dropna().str.split(',').explode().str.strip()
        print(all_skills.value_counts().head())


# ==========================================
# ГОЛОВНИЙ БЛОК ВИКОНАННЯ БУГА-ГА-ГАШЕЧКИ.
# ==========================================
if __name__ == "__main__":
    # Завдання 1
    prep = DataPreparation('it_jobs.db', 'Job opportunities.csv')
    prep.load_and_clean_data()
    prep.save_to_sqlite('jobs')

    connection = prep.get_connection()

    # Завдання 2
    basic = BasicQueries(connection)
    basic.run()

    # Завдання 3 та 4
    analytical = AnalyticalQueries(connection)
    analytical.run()

    # Завдання 5 та 6
    complex_q = ComplexQueries(connection, prep.df)
    complex_q.run()

    # Завдання 7. Закриття з'єднання
    connection.close()
    print("\nЗ'єднання з базою даних закрито.")