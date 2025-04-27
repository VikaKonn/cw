import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

class FinancialAnalyzer:
    def __init__(self, data_path="company_financial_data.csv"):
        self.df = pd.read_csv(data_path)
        self.df['Дата'] = pd.to_datetime(self.df['Год'].astype(str) + '-' + self.df['Месяц'].map({
            'Январь': '01', 'Февраль': '02', 'Март': '03', 'Апрель': '04',
            'Май': '05', 'Июнь': '06', 'Июль': '07', 'Август': '08',
            'Сентябрь': '09', 'Октябрь': '10', 'Ноябрь': '11', 'Декабрь': '12'
        }), format='%Y-%m')
        
    def analyze_trends(self):
        """Анализ трендов по годам"""
        yearly_data = self.df.groupby('Год').agg({
            'Выручка': 'mean',
            'Чистая прибыль': 'mean',
            'Рентабельность продаж': 'mean',
            'Доля рынка': 'mean'
        }).reset_index()
        
        plt.figure(figsize=(12, 8))
        for col in yearly_data.columns[1:]:
            plt.plot(yearly_data['Год'], yearly_data[col], marker='o', label=col)
        plt.title('Динамика ключевых показателей')
        plt.legend()
        plt.grid(True)
        plt.savefig('trends.png')
        plt.close()
        
    def analyze_seasonality(self):
        """Анализ сезонности"""
        monthly_data = self.df.groupby('Месяц').agg({
            'Выручка': 'mean',
            'Чистая прибыль': 'mean'
        }).reset_index()
        
        plt.figure(figsize=(12, 6))
        plt.bar(monthly_data['Месяц'], monthly_data['Выручка'])
        plt.title('Сезонность выручки')
        plt.xticks(rotation=45)
        plt.savefig('seasonality.png')
        plt.close()
        
    def analyze_departments(self):
        """Анализ подразделений"""
        dept_stats = self.df.groupby('Подразделение').agg({
            'Выручка': ['mean', 'std'],
            'Рентабельность продаж': 'mean',
            'Доля рынка': 'mean'
        }).round(2)
        
        # Топ-10 подразделений по выручке
        top_depts = self.df.groupby('Подразделение')['Выручка'].mean().nlargest(10)
        
        plt.figure(figsize=(12, 6))
        top_depts.plot(kind='bar')
        plt.title('Топ-10 подразделений по выручке')
        plt.xticks(rotation=45)
        plt.savefig('top_departments.png')
        plt.close()
        
        return dept_stats, top_depts
        
    def analyze_correlations(self):
        """Анализ корреляций между показателями"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        corr_matrix = self.df[numeric_cols].corr()
        
        plt.figure(figsize=(12, 10))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
        plt.title('Корреляционная матрица')
        plt.savefig('correlations.png')
        plt.close()
        
        return corr_matrix
        
    def detect_anomalies(self):
        """Выявление аномалий"""
        numeric_cols = ['Выручка', 'Чистая прибыль', 'Рентабельность продаж']
        anomalies = {}
        
        for col in numeric_cols:
            z_scores = np.abs(stats.zscore(self.df[col]))
            anomalies[col] = self.df[z_scores > 3]
            
        return anomalies
        
    def generate_report(self):
        """Генерация полного отчета"""
        self.analyze_trends()
        self.analyze_seasonality()
        dept_stats, top_depts = self.analyze_departments()
        corr_matrix = self.analyze_correlations()
        anomalies = self.detect_anomalies()
        
        report = {
            'Тренды': 'Сохранены в trends.png',
            'Сезонность': 'Сохранены в seasonality.png',
            'Статистика по подразделениям': dept_stats,
            'Топ подразделений': top_depts,
            'Корреляции': corr_matrix,
            'Аномалии': anomalies
        }
        
        return report

if __name__ == "__main__":
    analyzer = FinancialAnalyzer()
    report = analyzer.generate_report()
    print("Анализ завершен. Результаты сохранены в графиках и отчете.") 