import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (15, 6)

# ============================================================
# 1. Завантаження та створення датафрейму
# ============================================================
df = pd.read_csv('comptage_velo_2009.csv',
                 sep=',',
                 encoding='latin1',
                 parse_dates=['date'])

print("=" * 60)
print("ПЕРШІ 5 РЯДКІВ ДАТАФРЕЙМУ:")
print("=" * 60)
print(df.head())

print("\n" + "=" * 60)
print("ІНФОРМАЦІЯ ПРО ДАТАФРЕЙМ:")
print("=" * 60)
print(df.info())

print("\n" + "=" * 60)
print("СТАТИСТИЧНИЙ ОПИС:")
print("=" * 60)
print(df.describe())

# ============================================================
# 2. Загальна кількість велосипедистів за рік на всіх доріжках
# ============================================================
total_all = df['nb_passage'].sum()
print("\n" + "=" * 60)
print("ЗАГАЛЬНА КІЛЬКІСТЬ ВЕЛОСИПЕДИСТІВ (всі доріжки):")
print("=" * 60)
print(f"  Всього: {int(total_all):,} велосипедистів")

# ============================================================
# 3. Загальна кількість велосипедистів на кожній доріжці
# ============================================================
total_per_path = df.groupby('id_compteur')['nb_passage'].sum()
print("\n" + "=" * 60)
print("КІЛЬКІСТЬ ВЕЛОСИПЕДИСТІВ НА КОЖНІЙ ДОРІЖЦІ:")
print("=" * 60)
for path, count in total_per_path.items():
    print(f"  Доріжка {path}: {int(count):,} велосипедистів")

# ============================================================
# 4. Найпопулярніший місяць для трьох велодоріжок
# ============================================================
months_ua = {
    1: 'Січень',   2: 'Лютий',    3: 'Березень',
    4: 'Квітень',  5: 'Травень',  6: 'Червень',
    7: 'Липень',   8: 'Серпень',  9: 'Вересень',
    10: 'Жовтень', 11: 'Листопад', 12: 'Грудень'
}

# Додаємо колонку місяць
df['month'] = df['date'].dt.month

# Вибираємо три доріжки
selected_paths = total_per_path.index[:3].tolist()

print("\n" + "=" * 60)
print("НАЙПОПУЛЯРНІШИЙ МІСЯЦЬ ДЛЯ ТРЬОХ ВЕЛОДОРІЖОК:")
print("=" * 60)

for path in selected_paths:
    df_path = df[df['id_compteur'] == path]
    monthly = df_path.groupby('month')['nb_passage'].sum()
    best_month_num = monthly.idxmax()
    best_month_name = months_ua[best_month_num]
    best_count = int(monthly.max())
    print(f"  Доріжка {path}:")
    print(f"    Найпопулярніший місяць: {best_month_name} "
          f"({best_count:,} велосипедистів)")

# ============================================================
# 5. Графік завантаженості однієї велодоріжки по місяцям
# ============================================================
chosen_path = selected_paths[0]
df_chosen = df[df['id_compteur'] == chosen_path]
monthly_data = df_chosen.groupby('month')['nb_passage'].sum()

month_labels = [months_ua[m] for m in monthly_data.index]

fig, ax = plt.subplots(figsize=(15, 6))

bars = ax.bar(
    range(len(monthly_data)),
    monthly_data.values,
    color='steelblue',
    edgecolor='navy',
    alpha=0.8
)

# Підписи значень над стовпчиками
for bar, value in zip(bars, monthly_data.values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + max(monthly_data.values) * 0.01,
        f'{int(value):,}',
        ha='center',
        va='bottom',
        fontsize=9,
        fontweight='bold'
    )

ax.set_xticks(range(len(monthly_data)))
ax.set_xticklabels(month_labels, rotation=30, ha='right', fontsize=11)
ax.set_xlabel('Місяць', fontsize=13)
ax.set_ylabel('Кількість велосипедистів', fontsize=13)
ax.set_title(
    f'Завантаженість велодоріжки {chosen_path} по місяцям (2009 рік)',
    fontsize=14,
    fontweight='bold'
)

plt.tight_layout()
plt.savefig('bike_path_2009.png', dpi=150, bbox_inches='tight')
plt.show()
print("\nГрафік збережено: bike_path_2009.png")
