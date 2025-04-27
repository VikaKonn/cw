import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt

# Настройка страницы
st.set_page_config(
    page_title="Анализ финансовой отчетности",
    page_icon="📊",
    layout="wide"
)

# Заголовок
st.title("📊 Система анализа финансовой отчетности предприятия")

# Загрузка данных
@st.cache_data
def load_data():
    return pd.read_csv("company_financial_data.csv")

data = load_data()

# Сайдбар для фильтров
with st.sidebar:
    st.header("Фильтры")
    
    # Выбор периода
    years = sorted(data['Год'].unique())
    year_range = st.slider(
        "Выберите период",
        min_value=min(years),
        max_value=2025,
        value=(min(years), 2025)
    )
    
    # Выбор подразделений
    subdivisions = sorted(data['Подразделение'].unique())
    selected_subdivisions = st.multiselect(
        "Выберите подразделения",
        subdivisions,
        default=subdivisions[:5]
    )
    
    # Выбор показателей
    metrics = [
        'Выручка', 'Чистая прибыль', 'Операционные расходы',
        'Активы', 'Обязательства', 'Коэффициент текущей ликвидности',
        'Доля рынка', 'Количество сотрудников', 'Рентабельность продаж',
        'Оборачиваемость активов', 'Рентабельность активов', 'Долговая нагрузка'
    ]
    selected_metrics = st.multiselect(
        "Выберите показатели для анализа",
        metrics,
        default=['Выручка', 'Чистая прибыль']
    )

# Фильтрация данных
filtered_data = data[
    (data['Год'].between(year_range[0], year_range[1])) &
    (data['Подразделение'].isin(selected_subdivisions))
]

# Основные вкладки
tab1, tab2, tab3, tab4 = st.tabs(["Общая статистика", "Анализ подразделений", "Временной анализ", "Прогнозирование"])

with tab1:
    st.header("Общая статистика")
    
    # Сводная таблица
    st.subheader("Сводная статистика")
    st.dataframe(filtered_data[selected_metrics].describe())
    
    # Графики распределения
    st.subheader("Распределение показателей")
    for metric in selected_metrics:
        fig = px.histogram(filtered_data, x=metric, title=f"Распределение {metric}")
        st.plotly_chart(fig, use_container_width=True)
    
    # Корреляционная матрица
    st.subheader("Корреляционная матрица")
    corr_matrix = filtered_data[selected_metrics].corr()
    fig = px.imshow(corr_matrix, text_auto=True, aspect="auto")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Анализ подразделений")
    
    # Топ подразделений по выручке
    st.subheader("Топ подразделений по выручке")
    top_revenue = filtered_data.groupby('Подразделение')['Выручка'].mean().sort_values(ascending=False).head(10)
    fig = px.bar(top_revenue, title="Топ-10 подразделений по средней выручке")
    st.plotly_chart(fig, use_container_width=True)
    
    # Сравнение подразделений
    st.subheader("Сравнение подразделений")
    for metric in selected_metrics:
        fig = px.box(filtered_data, x='Подразделение', y=metric, title=f"Распределение {metric} по подразделениям")
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Временной анализ")
    
    # Тренды по годам
    st.subheader("Тренды по годам")
    yearly_data = filtered_data.groupby('Год')[selected_metrics].mean().reset_index()
    fig = px.line(yearly_data, x='Год', y=selected_metrics, title="Динамика показателей по годам")
    st.plotly_chart(fig, use_container_width=True)
    
    # Сезонность по месяцам
    st.subheader("Сезонность по месяцам")
    monthly_data = filtered_data.groupby('Месяц')[selected_metrics].mean().reset_index()
    fig = px.line(monthly_data, x='Месяц', y=selected_metrics, title="Сезонность показателей")
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.header("Прогнозирование")
    
    # Выбор модели
    model_type = st.selectbox(
        "Выберите модель для прогнозирования",
        ["Линейная регрессия", "Случайный лес"]
    )
    
    # Выбор показателя для прогноза
    target_metric = st.selectbox(
        "Выберите показатель для прогноза",
        selected_metrics
    )
    
    # Настройка параметров
    forecast_years = st.slider(
        "Количество лет для прогноза",
        min_value=1,
        max_value=3,
        value=3
    )
    
    # Кнопка для запуска прогноза
    if st.button("Сделать прогноз"):
        st.info("Прогнозирование...")
        
        # Получаем последний год из данных
        last_year = filtered_data['Год'].max()
        
        # Создаем список лет для прогноза
        forecast_years_list = [last_year + i + 1 for i in range(forecast_years)]
        
        # Рассчитываем средний годовой прирост на основе исторических данных
        yearly_means = filtered_data.groupby('Год')[target_metric].mean()
        yearly_growth = yearly_means.pct_change().mean()
        
        # Если рост отрицательный или слишком большой, используем более консервативную оценку
        if yearly_growth < 0 or yearly_growth > 0.15:
            yearly_growth = 0.05  # 5% годовой рост
        
        # Генерируем прогнозные значения на основе последнего известного значения
        last_value = yearly_means.iloc[-1]
        forecast_values = []
        for i in range(forecast_years):
            next_value = last_value * (1 + yearly_growth)
            forecast_values.append(next_value)
            last_value = next_value
        
        # Временный график для демонстрации
        fig = go.Figure()
        
        # Исторические данные
        historical_years = filtered_data['Год'].unique()
        historical_values = filtered_data.groupby('Год')[target_metric].mean()
        
        fig.add_trace(go.Scatter(
            x=historical_years,
            y=historical_values,
            name='Исторические данные',
            mode='lines+markers'
        ))
        
        fig.add_trace(go.Scatter(
            x=forecast_years_list,
            y=forecast_values,
            name='Прогноз',
            line=dict(dash='dash'),
            mode='lines+markers'
        ))
        
        # Настройка внешнего вида графика
        fig.update_layout(
            title=f"Прогноз {target_metric} на {forecast_years} лет",
            xaxis_title="Год",
            yaxis_title=target_metric,
            showlegend=True,
            xaxis=dict(
                dtick=1,
                tickmode='linear'
            )
        )
        
        st.success("Прогноз готов!")
        st.plotly_chart(fig, use_container_width=True)

# Футер
st.markdown("---")
st.markdown("© 2025 Система анализа финансовой отчетности")
st.markdown("Разработано: Коновалова Виктория") 