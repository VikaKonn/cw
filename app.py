import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
from sklearn.preprocessing import StandardScaler

# Загрузка модели
@st.cache_data
def load_model():
    return joblib.load("trained_model.joblib")

# Настройка страницы
st.set_page_config(
    page_title="Анализ финансовой отчетности",
    layout="wide"
)

# Заголовок
st.title("Система анализа финансовой отчетности предприятия")

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

    # Выбор метрики
    target = st.radio("Что вы хотите спрогнозировать?", ["Чистая прибыль", "Выручка"])
    model_path = "model_profit.joblib" if target == "Чистая прибыль" else "model_revenue.joblib"
    model = joblib.load(model_path)

    # Ввод пользователем количества лет
    years_to_predict = st.slider("Сколько лет вперёд спрогнозировать?", 1, 10, 3)

    # Загрузка данных и определение последнего года
    df = pd.read_csv("company_financial_data.csv")
    last_year = df["Год"].max()
    future_years = np.array(range(last_year + 1, last_year + years_to_predict + 1)).reshape(-1, 1)

    # Прогнозирование
    forecast = model.predict(future_years)

    # Отображение
    forecast_df = pd.DataFrame({
        "Год": future_years.flatten(),
        "Прогноз": forecast.astype(int)
    })
    forecast_df.reset_index(drop=True, inplace=True)

    st.subheader(f"Прогноз на {target.lower()} на {years_to_predict} лет:")
    st.dataframe(forecast_df.style.format({"Год": "{:d}"}), hide_index=True)

    # Для графика — преобразуем год в строку, чтобы не было разделителя тысяч
    forecast_df_plot = forecast_df.copy()
    forecast_df_plot["Год"] = forecast_df_plot["Год"].astype(str)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=forecast_df["Год"].astype(str),  # делаем года строкой для дискретной оси
        y=forecast_df["Прогноз"],
        mode='lines+markers'
    ))
    fig.update_layout(
        xaxis_title="Год",
        yaxis_title="Прогноз",
        xaxis_tickangle=0,
        xaxis_type="category"  # вот это важно!
    )
    st.plotly_chart(fig, use_container_width=True)

# Футер
st.markdown("---")
st.markdown("© 2025 Система анализа финансовой отчетности")
st.markdown("Разработано: Коновалова Виктория") 