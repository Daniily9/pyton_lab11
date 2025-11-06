import pandas as pd
from datetime import time
import json # Для гарного виведення словника

# --- 1. Створення та доповнення словника ---
# (Базується на словнику з Практичної роботи №5)
# Додано нові поля: 'train_type' (для групування)
# та 'platform' (для числових операцій)

schedule = {
    "128К": {
        "destination": "Київ - Харків",
        "arrival": time(10, 30),
        "departure": time(10, 50),
        "train_type": "Intercity", # Додано
        "platform": 5             # Додано
    },
    "046Д": {
        "destination": "Львів - Одеса",
        "arrival": time(14, 5),
        "departure": time(14, 25),
        "train_type": "Night Express",
        "platform": 2
    },
    "749О": {
        "destination": "Київ - Івано-Франківськ",
        "arrival": time(8, 15),
        "departure": time(8, 30),
        "train_type": "Intercity",
        "platform": 9
    },
    "001М": {
        "destination": "Мінськ - Київ",
        "arrival": time(23, 50), # Стоїть "через північ"
        "departure": time(0, 20),
        "train_type": "International",
        "platform": 1
    },
    "081К": {
        "destination": "Київ - Ужгород",
        "arrival": time(17, 0),
        "departure": time(17, 22),
        "train_type": "Night Express",
        "platform": 7
    },
    "012П": {
        "destination": "Одеса - Львів",
        "arrival": time(2, 40),
        "departure": time(3, 0),
        "train_type": "Night Express",
        "platform": 3
    },
    "092К": {
        "destination": "Київ - Варшава",
        "arrival": time(19, 10),
        "departure": time(19, 35),
        "train_type": "International",
        "platform": 1
    },
    "142Ш": {
        "destination": "Бахмут - Львів",
        "arrival": time(12, 12),
        "departure": time(12, 32),
        "train_type": "Regional",
        "platform": 10
    },
    "007Д": {
        "destination": "Київ - Чернівці",
        "arrival": time(20, 5),
        "departure": time(20, 25),
        "train_type": "Night Express",
        "platform": 4
    },
    "110Л": {
        "destination": "Львів - Херсон",
        "arrival": time(22, 10),
        "departure": time(22, 30),
        "train_type": "Night Express",
        "platform": 6
    },
    # --- Додаткові записи для кращого аналізу ---
    "070Л": {
        "destination": "Львів - Маріуполь",
        "arrival": time(15, 30),
        "departure": time(15, 55),
        "train_type": "Night Express",
        "platform": 2
    },
    "771К": {
        "destination": "Київ - Хмельницький",
        "arrival": time(6, 5),
        "departure": time(6, 10),
        "train_type": "Intercity",
        "platform": 8
    }
}

print("=== 🚂 1. Вміст доповненого словника 'schedule' ===")
# Використовуємо json для читабельного виводу словника
print(json.dumps(schedule, default=str, indent=4, ensure_ascii=False))

print("\n" + "="*50 + "\n")

# --- 2. Перетворення словника на DataFrame ---
# Використовуємо orient='index', щоб ключі словника (номери поїздів)
# стали індексом DataFrame.
df = pd.DataFrame.from_dict(schedule, orient='index')
df.index.name = 'train_number' # Даємо назву індексу

print("=== 2. Створений DataFrame з розкладом ===")
print(df)

print("\n" + "="*50 + "\n")

# --- 3. Базовий аналіз даних ---
print("=== 3. Базовий аналіз даних ===")

print("\n--- 3.1. Перші 3 рядки (df.head(3)) ---")
print(df.head(3))

print("\n--- 3.2. Типи даних (df.dtypes) ---")
# Зверніть увагу, 'arrival' і 'departure' мають тип 'object',
# оскільки вони містять об'єкти Python 'datetime.time'.
print(df.dtypes)

print("\n--- 3.3. Кількість рядків і стовпців (df.shape) ---")
rows, cols = df.shape
print(f"Кількість рядків: {rows}")
print(f"Кількість стовпців: {cols}")

print("\n--- 3.4. Описова статистика (df.describe()) ---")
# df.describe() автоматично аналізує лише числові стовпці (в нашому випадку 'platform')
print(df.describe())

print("\n" + "="*50 + "\n")

# --- 4. Додавання нового розрахункового стовпця ---
# Обчислимо тривалість стоянки ('stop_duration')
print("=== 4. Додавання розрахункового стовпця 'stop_duration' ===")

# Допоміжна функція для конвертації time в timedelta (для обчислень)
def time_to_timedelta(t):
    if pd.isna(t):
        return pd.NaT
    return pd.to_timedelta(f"{t.hour}h {t.minute}m {t.second}s")

# Конвертуємо стовпці часу в 'timedelta'
arrival_td = df['arrival'].apply(time_to_timedelta)
departure_td = df['departure'].apply(time_to_timedelta)

# Розраховуємо тривалість
duration = departure_td - arrival_td

# Обробка випадку "через північ" (коли тривалість від'ємна)
one_day = pd.to_timedelta('24h')
# Якщо тривалість негативна, додаємо 24 години
df['stop_duration'] = duration.apply(
    lambda td: td if td.total_seconds() >= 0 else td + one_day
)

print(df[['destination', 'arrival', 'departure', 'stop_duration']])

print("\n" + "="*50 + "\n")

# --- 5. Фільтрація даних ---
print("=== 5. Фільтрація: поїзди 'Intercity' з платформою > 5 ===")
# Приклад: виберемо поїзди типу 'Intercity', які прибувають на платформу > 5
filtered_df = df[
    (df['train_type'] == 'Intercity') & (df['platform'] > 5)
]
print(filtered_df)

print("\n=== 5.1. Фільтрація: поїзди зі стоянкою > 20 хвилин ===")
long_stops = df[df['stop_duration'] > pd.to_timedelta('20 minutes')]
print(long_stops[['destination', 'stop_duration']])

print("\n" + "="*50 + "\n")

# --- 6. Сортування даних ---
print("=== 6. Сортування: за тривалістю стоянки (за спаданням) ===")
df_sorted = df.sort_values(by='stop_duration', ascending=False)
print(df_sorted[['destination', 'train_type', 'stop_duration']])

print("\n" + "="*50 + "\n")

# --- 7. Групування даних та середнє значення ---
print("=== 7. Групування: середня тривалість стоянки за типом поїзда ===")
# Групуємо за 'train_type' і знаходимо середнє
avg_duration_by_type = df.groupby('train_type')['stop_duration'].mean()
print(avg_duration_by_type)

print("\n=== 7.1. Групування: середня платформа за типом поїзда ===")
avg_platform_by_type = df.groupby('train_type')['platform'].mean()
print(avg_platform_by_type)

print("\n" + "="*50 + "\n")

# --- 8. Додаткові операції агрегації ---
print("=== 8. Додаткові операції агрегації ===")

print("\n--- 8.1. Статистика за типом поїзда ---")
# Використовуємо .agg() для кількох операцій одночасно
agg_stats = df.groupby('train_type').agg(
    train_count=pd.NamedAgg(column='destination', aggfunc='count'),
    max_stop_duration=pd.NamedAgg(column='stop_duration', aggfunc='max'),
    min_stop_duration=pd.NamedAgg(column='stop_duration', aggfunc='min'),
    avg_platform=pd.NamedAgg(column='platform', aggfunc='mean')
)
print(agg_stats)

print("\n--- 8.2. Кількість унікальних значень ---")
unique_train_types = df['train_type'].nunique()
print(f"Кількість унікальних типів поїздів: {unique_train_types}")

unique_destinations = df['destination'].nunique()
print(f"Кількість унікальних напрямків: {unique_destinations}")
