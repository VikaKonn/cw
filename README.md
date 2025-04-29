# Анализ Финансовых Данных Компаний

Проект для анализа финансовых данных компаний с использованием машинного обучения и интерактивного веб-интерфейса на Streamlit.

## Возможности
- Анализ финансовых данных
- Прогнозирование с помощью ML
- Интерактивная веб-панель

## Установка
1. Клонируйте репозиторий
2. Создайте виртуальное окружение:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```
3. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Использование
Запустите Streamlit приложение:
```bash
streamlit run app.py
```

## Структура проекта
- `app.py` - Веб-приложение на Streamlit
- `analysis.py` - Функции анализа данных
- `data.py` - Утилиты для обработки данных
- `trained_model.joblib` - Сохраненная ML модель
- `company_financial_data.csv` - Набор данных 