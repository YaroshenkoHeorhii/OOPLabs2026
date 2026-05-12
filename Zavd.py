# Ярошенко Георгій

import pandas as pd
import re


class DataLoader:
    """1. Клас для імпорту та первинного аналізу даних """

    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def load(self):
        # Завантаження CSV
        self.df = pd.read_csv(self.file_path)
        # Очищення назв стовпців від зайвих пробілів
        self.df.columns = self.df.columns.str.strip()
        return self.df

    def primary_analysis(self):
        print("--- Перші 5 рядків ---")
        print(self.df.head(5))
        print("\n--- Останні 5 рядків ---")
        print(self.df.tail(5))

        rows, cols = self.df.shape
        print(f"\nРозмірність: {rows} рядків, {cols} стовпців ")

        mem = self.df.memory_usage(deep=True).sum() / (1024 ** 2)
        print(f"Обсяг пам'яті: {mem:.2f} MB ")

    def check_structure(self):
        print("\n--- Типи даних ---")
        print(self.df.dtypes)
        print("\n--- Пропущені значення ---")
        print(self.df.isnull().sum())


class DataCleaner:
    """2. Клас для перетворення типів даних """

    @staticmethod
    def process_salary(df):
        # Витягуємо максимальне значення з текстового Salary Range
        def extract_max(text):
            # Знаходимо всі числа, видаляючи коми та символи валют
            numbers = re.findall(r'\d+', str(text).replace(',', ''))
            if numbers:
                return int(numbers[-1])  # Беремо останнє число як максимальне
            return 0

        def extract_min(text):
            numbers = re.findall(r'\d+', str(text).replace(',', ''))
            if numbers:
                return int(numbers[0])  # Беремо перше число як мінімальне
            return 0

        df['Max Salary'] = df['Salary Range'].apply(extract_max)
        df['Min Salary'] = df['Salary Range'].apply(extract_min)
        return df

    @staticmethod
    def process_dates(df):
        # Перетворення у datetime та створення колонки Year
        df['Date Posted'] = pd.to_datetime(df['Date Posted'])
        df['Year'] = df['Date Posted'].dt.year
        return df


class DataFilter:
    """3. Клас для фільтрації вакансій """

    @staticmethod
    def by_industry(df, industry):
        return df[df['Industry'] == industry]

    @staticmethod
    def by_level(df, level):
        return df[df['Experience Level'] == level]

    @staticmethod
    def by_type_and_city(df, job_type, city):
        # Використовуємо 'Job Type' (згідно з вашим файлом)
        return df[(df['Job Type'] == job_type) & (df['Location'] == city)]


class DataAnalyzer:
    """4. Клас для аналітики та групування """

    @staticmethod
    def get_top_salaries(df, n=5):
        return df.sort_values(by='Max Salary', ascending=False).head(n)

    @staticmethod
    def industry_stats(df):
        # Групування за галузями: кількість та середня мін. зарплата
        stats = df.groupby('Industry').agg(
            count=('Job Title', 'count'),
            avg_min_salary=('Min Salary', 'mean')
        )
        return stats.sort_values(by='avg_min_salary', ascending=False)

    @staticmethod
    def add_salary_category(df):
        # Категоризація за допомогою apply()
        def categorize(val):
            if val <= 40000:
                return 'Low'
            elif val <= 70000:
                return 'Medium'
            return 'High'

        df['Salary Category'] = df['Max Salary'].apply(categorize)
        return df

    @staticmethod
    def yearly_analysis(df):
        # Аналіз активності за роками
        return df.groupby('Year').agg(count=('Job Title', 'count')).sort_values(by='count', ascending=False)


# Виконання програми
if __name__ == "__main__":
    # Імпорт
    handler = DataLoader('Job opportunities.csv')
    df = handler.load()
    handler.primary_analysis()
    handler.check_structure()

    # Очищення
    df = DataCleaner.process_salary(df)
    df = DataCleaner.process_dates(df)

    # Фільтрація
    print("\n--- Вакансії Cloud Computing ---")
    print(DataFilter.by_industry(df, 'Cloud Computing').head())

    # Сортування
    print("\n--- ТОП-5 зарплат ---")
    print(DataAnalyzer.get_top_salaries(df))

    # Групування
    print("\n--- Статистика по галузях (ТОП) ---")
    print(DataAnalyzer.industry_stats(df).head())

    # Категоризація
    df = DataAnalyzer.add_salary_category(df)
    print("\n--- Перевірка категорій зарплат ---")
    print(df[['Max Salary', 'Salary Category']].head())

    # Часовий аналіз
    print("\n--- Активність за роками ---")
    print(DataAnalyzer.yearly_analysis(df))