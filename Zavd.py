# Ярошенко Георгій

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class JobDataVisualizer:
    def __init__(self, file_path):
        """Ініціалізація та завантаження даних."""
        try:
            self.df = pd.read_csv(file_path)
            self.prepare_data()
            print("Дані успішно завантажено та підготовлено.")
        except FileNotFoundError:
            print(f"Помилка: Файл за адресою '{file_path}' не знайдено. Перевірте шлях до файлу!")
            self.df = None

    def prepare_data(self):
        """Підготовка даних: очищення та створення нових ознак."""
        if self.df is None:
            return

        # 1. Розрахунок середньої зарплати (Average Salary)
        # Використовуємо r'(\d+)' для уникнення SyntaxWarning
        if 'Salary Range' in self.df.columns:
            salaries = self.df['Salary Range'].str.extractall(r'(\d+)').unstack().astype(float)
            self.df['Average Salary'] = salaries.mean(axis=1)

        # 2. Витягування року для часового аналізу
        if 'Date Posted' in self.df.columns:
            self.df['Year'] = pd.to_datetime(self.df['Date Posted']).dt.year

    def plot_barplot(self):
        """Стовпчаста діаграма: середня зарплата vs досвід."""
        plt.figure(figsize=(10, 6))
        # Додано hue та legend=False для виправлення FutureWarning
        sns.barplot(
            x='Experience Level',
            y='Average Salary',
            data=self.df,
            hue='Experience Level',
            palette='viridis',
            legend=False
        )
        plt.title('Середня зарплата за рівнем досвіду')
        plt.xlabel('Рівень досвіду')
        plt.ylabel('Середня зарплата ($)')
        plt.show()

    def plot_boxplot(self):
        """Діаграма розмаху: розподіл зарплат за галузями."""
        plt.figure(figsize=(12, 6))
        # Додано hue та legend=False для виправлення FutureWarning
        sns.boxplot(
            x='Industry',
            y='Average Salary',
            data=self.df,
            hue='Industry',
            palette='Set2',
            legend=False
        )
        plt.xticks(rotation=45, ha='right')
        plt.title('Розподіл зарплат за галузями')
        plt.xlabel('Галузь')
        plt.ylabel('Зарплата ($)')
        plt.tight_layout()
        plt.show()

    def plot_heatmap(self):
        """Теплова карта: кількість вакансій за категоріями."""
        pivot_table = pd.crosstab(self.df['Experience Level'], self.df['Industry'])
        plt.figure(figsize=(12, 8))
        sns.heatmap(pivot_table, annot=True, cmap='YlGnBu', fmt='d')
        plt.title('Кількість вакансій: Досвід vs Галузь')
        plt.show()

    def plot_scatterplot(self):
        """Точковий графік: динаміка зарплат за роками."""
        plt.figure(figsize=(10, 6))
        sns.scatterplot(
            x='Year',
            y='Average Salary',
            hue='Experience Level',
            data=self.df,
            palette='deep'
        )
        plt.title('Тенденція зарплат за роками (2019-2023)')
        plt.xlabel('Рік')
        plt.ylabel('Зарплата ($)')
        plt.legend(title='Рівень досвіду', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()

    def plot_pairplot(self):
        """Парні графіки для виявлення взаємозв'язків."""
        cols = ['Average Salary', 'Year', 'Experience Level']
        subset = self.df[cols].dropna()
        sns.pairplot(subset, hue='Experience Level', palette='bright')
        plt.show()


# --- Головний блок виконання ---
if __name__ == "__main__":
    FILE_PATH = 'Job opportunities.csv'
    visualizer = JobDataVisualizer(FILE_PATH)

    if visualizer.df is not None:
        visualizer.plot_barplot()
        visualizer.plot_boxplot()
        visualizer.plot_heatmap()
        visualizer.plot_scatterplot()
        visualizer.plot_pairplot()  # <-- Тут не вистачало дужок