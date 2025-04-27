import pandas as pd
import numpy as np
from datetime import datetime

# Параметры
years = range(2018, 2028)
months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", 
          "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
departments = [f"Подразделение_{i}" for i in range(1, 126)]

# Генерация данных с трендами и сезонностью
np.random.seed(42)
data = {
    "Год": [],
    "Месяц": [],
    "Подразделение": [],
    "Выручка": [],
    "Чистая прибыль": [],
    "Операционные расходы": [],
    "Активы": [],
    "Обязательства": [],
    "Коэффициент текущей ликвидности": [],
    "Доля рынка": [],
    "Количество сотрудников": [],
    "Рентабельность продаж": [],
    "Оборачиваемость активов": [],
    "Рентабельность активов": [],
    "Долговая нагрузка": []
}

# Сезонные коэффициенты (пики в декабре и июне)
seasonal_factors = {
    "Январь": 0.8, "Февраль": 0.85, "Март": 0.9, "Апрель": 0.95,
    "Май": 1.0, "Июнь": 1.2, "Июль": 1.1, "Август": 1.0,
    "Сентябрь": 0.95, "Октябрь": 0.9, "Ноябрь": 0.95, "Декабрь": 1.3
}

for year in years:
    year_factor = 1 + (year - 2018) * 0.05  # Годовой рост 5%
    for month in months:
        month_factor = seasonal_factors[month]
        for department in departments:
            # Базовые значения с трендом и сезонностью
            base_revenue = np.random.uniform(1000000, 2000000) * year_factor * month_factor
            base_assets = np.random.uniform(200000, 500000) * year_factor
            
            data["Год"].append(year)
            data["Месяц"].append(month)
            data["Подразделение"].append(department)
            data["Выручка"].append(round(base_revenue, 2))
            
            # Операционные расходы зависят от выручки
            expenses_ratio = np.random.uniform(0.6, 0.8)
            data["Операционные расходы"].append(round(base_revenue * expenses_ratio, 2))
            
            # Чистая прибыль с учетом налогов
            tax_rate = 0.2
            data["Чистая прибыль"].append(round(base_revenue * (1 - expenses_ratio) * (1 - tax_rate), 2))
            
            data["Активы"].append(round(base_assets, 2))
            
            # Обязательства зависят от активов
            liabilities_ratio = np.random.uniform(0.4, 0.6)
            data["Обязательства"].append(round(base_assets * liabilities_ratio, 2))
            
            # Расчетные показатели
            current_assets = base_assets * np.random.uniform(0.4, 0.6)
            current_liabilities = base_assets * liabilities_ratio * np.random.uniform(0.3, 0.5)
            data["Коэффициент текущей ликвидности"].append(round(current_assets / current_liabilities, 2))
            
            # Доля рынка с небольшим ростом
            market_share = np.random.uniform(10, 20) * (1 + (year - 2018) * 0.01)
            data["Доля рынка"].append(round(market_share, 2))
            
            # Количество сотрудников с учетом роста
            employees = np.random.randint(200, 500) * (1 + (year - 2018) * 0.02)
            data["Количество сотрудников"].append(int(employees))
            
            # Дополнительные финансовые показатели
            revenue = data["Выручка"][-1]
            profit = data["Чистая прибыль"][-1]
            assets = data["Активы"][-1]
            liabilities = data["Обязательства"][-1]
            
            data["Рентабельность продаж"].append(round(profit / revenue * 100, 2))
            data["Оборачиваемость активов"].append(round(revenue / assets, 2))
            data["Рентабельность активов"].append(round(profit / assets * 100, 2))
            data["Долговая нагрузка"].append(round(liabilities / assets * 100, 2))

# Создание DataFrame
df = pd.DataFrame(data)

# Добавление случайных выбросов (5% данных)
outlier_mask = np.random.random(len(df)) < 0.05
df.loc[outlier_mask, "Выручка"] *= np.random.uniform(1.5, 3)
df.loc[outlier_mask, "Чистая прибыль"] *= np.random.uniform(1.5, 3)

# Сохранение в CSV
df.to_csv("company_financial_data.csv", index=False)

print("Датасет успешно создан!")