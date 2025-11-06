import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import calendar # Для отримання назв місяців

print("=== 🚴 Аналіз велодоріжок Монреаля (2009 рік) ===")

# --- 1. Завантаження даних ---

# Використовуємо ім'я файлу, яке ви вказали
file_name = "comptagevelo2009.csv"

try:
    # Читаємо локальний файл
    # parse_dates=['Date'] -> намагаємося перетворити стовпець 'Date' на дату
    # dayfirst=True -> вказуємо, що формат дати DD/MM/YYYY (європейський)
    df = pd.read_csv(file_name, parse_dates=['Date'], dayfirst=True)
    
    print(f"✅ Дані з файлу '{file_name}' успішно завантажено.\n")

    # --- 2. Перевірка основних характеристик ---
    print("--- 2.1. Перші 5 рядків (df.head()) ---")
    print(df.head())
    
    print("\n--- 2.2. Інформація про DataFrame (df.info()) ---")
    # df.info() покаже, чи є пропуски, і чи правильно розпізнано 'Date'
    df.info()

    print("\n--- 2.3. Описова статистика (df.describe()) ---")
    # df.describe() рахує статистику (середнє, мін/макс) для числових стовпців
    print(df.describe())
    print("\n" + "="*50 + "\n")

    # --- Підготовка даних ---
    # Встановлюємо 'Date' як індекс (це зручно для аналізу часових даних)
    df = df.set_index('Date')
    
    # Заповнюємо пропущені значення (NaN) нулями, щоб суми рахувалися коректно
    df = df.fillna(0)
    
    # Отримуємо список стовпців лічильників (всі стовпці)
    counter_columns = df.columns
    
    # Перетворюємо всі лічильники на цілі числа (int)
    df[counter_columns] = df[counter_columns].astype(int)

    # --- 3. Загальна кількість велосипедистів за рік (усі доріжки) ---
    # .sum() спочатку рахує суму по кожному стовпцю, 
    # а другий .sum() додає ці суми разом.
    total_all_cyclists = df[counter_columns].sum().sum()
    print("--- 3. Загальна кількість велосипедистів за рік (усі доріжки) ---")
    # : ,.0f -> форматує число з комами-роздільниками (напр., 1,234,567)
    print(f"Всього за 2009 рік на всіх доріжках: {total_all_cyclists:,.0f} велосипедистів\n")

    # --- 4. Загальна кількість велосипедистів за рік (кожна доріжка) ---
    total_per_path = df[counter_columns].sum()
    print("--- 4. Загальна кількість за рік (на кожній доріжці) ---")
    print(total_per_path.to_string(float_format='{:,.0f}'.format))
    print("\n" + "="*50 + "\n")

    # --- 5. Найпопулярніший місяць (для 3 обраних доріжок) ---
    print("--- 5. Найпопулярніший місяць (для 3 обраних доріжок) ---")
    
    # Створюємо копію, щоб не змінювати оригінальний df
    df_monthly = df.copy()
    
    # Створюємо новий стовпець 'Month' з номером місяця (1-12)
    df_monthly['Month'] = df_monthly.index.month
    
    # Групуємо дані по місяцю і сумуємо всі поїздки для кожного місяця
    monthly_counts = df_monthly.groupby('Month')[counter_columns].sum()
    
    # Змінюємо індекси (1, 2, 3...) на назви місяців ("January", "February"...)
    monthly_counts.index = [calendar.month_name[i] for i in monthly_counts.index]
    
    # Обираємо 3 доріжки для аналізу (наприклад, перші 3)
    paths_to_check = counter_columns[0:3] 
    
    for path in paths_to_check:
        # .idxmax() знаходить індекс (назву місяця) з максимальним значенням
        most_popular_month = monthly_counts[path].idxmax()
        count = monthly_counts[path].max()
        print(f"  ➡️  Доріжка '{path}': Найпопулярніший місяць = {most_popular_month} ({count:,.0f} велосипедистів)")
    
    print("\n" + "="*50 + "\n")

    # --- 6. Графік завантаженості однієї велодоріжки по місяцях ---
    print("--- 6. Побудова графіка завантаженості... ---")
    
    # Обираємо першу доріжку для побудови графіка
    path_to_plot = counter_columns[0]
    data_to_plot = monthly_counts[path_to_plot]
    
    # Створюємо "полотно" для малювання
    plt.figure(figsize=(12, 7))
    
    # Малюємо лінійний графік з маркерами
    data_to_plot.plot(kind='line', marker='o', linestyle='--')
    
    # 
    
    # Налаштування графіка
    plt.title(f"Завантаженість велодоріжки '{path_to_plot}' по місяцях (2009)", fontsize=16)
    plt.xlabel("Місяць", fontsize=12)
    plt.ylabel("Кількість велосипедистів", fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.7) # Додаємо сітку
    
    # Форматуємо вісь Y, щоб числа були з комами (напр., 10,000)
    ax = plt.gca() # Get Current Axis
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    plt.xticks(rotation=45) # Повертаємо назви місяців
    plt.tight_layout() # Автоматично налаштовує відступи
    
    # Зберігаємо графік у файл
    plot_filename = f"bike_usage_{path_to_plot.replace(' ', '_')}_2009.png"
    plt.savefig(plot_filename)
    print(f"✅ Графік збережено у файл: {plot_filename}")
    
    # Показуємо графік у вікні
    plt.show()

except FileNotFoundError:
    print(f"ПОМИЛКА: Файл '{file_name}' не знайдено.")
    print("Переконайтеся, що файл знаходиться у тій самій папці, що й ваш .py скрипт,")
    print("і що ім'я файлу написано правильно.")
except pd.errors.EmptyDataError:
    print(f"ПОМИЛКА: Файл '{file_name}' порожній.")
except Exception as e:
    print(f"Сталася неочікувана помилка: {e}")
    print("Можливо, файл пошкоджений або має неправильний формат.")
