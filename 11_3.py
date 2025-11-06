import nltk
import string
import matplotlib.pyplot as plt

# --- 1. Завантаження необхідних ресурсів NLTK ---
# Завантажуємо корпус Gutenberg (де знаходяться тексти)
nltk.download('gutenberg')
# Завантажуємо список стоп-слів (займенники, артиклі тощо)
nltk.download('stopwords')
# Завантажуємо токенізатор (для коректного розділення на слова та пунктуацію)
nltk.download('punkt')

print("=== 📖 Аналіз тексту 'carroll-alice.txt' (Варіант 19) ===\n")

# --- 2. Імпорт тексту з Project Gutenberg ---
try:
    # Завантажуємо список слів з обраного тексту
    words = nltk.corpus.gutenberg.words('carroll-alice.txt')
    
    # --- 3. Визначення кількості слів у тексті ---
    word_count = len(words)
    print(f"--- 3. Загальна кількість слів у тексті: {word_count} ---\n")

    # --- 4. 10 найбільш вживаних слів (до очищення) ---
    print("--- 4. 10 найбільш вживаних слів (ДО очищення) ---")
    
    # Переводимо всі слова у нижній регістр для коректного підрахунку
    words_lower = [word.lower() for word in words]
    
    # Рахуємо частоту кожного слова
    freq_dist_before = nltk.FreqDist(words_lower)
    
    # Отримуємо 10 найпопулярніших
    most_common_before = freq_dist_before.most_common(10)
    
    for word, count in most_common_before:
        print(f"  {word}: {count} разів")

    # --- 5. Побудова діаграми (до очищення) ---
    # Готуємо дані для графіка
    words_b, counts_b = zip(*most_common_before)
    
    plt.figure(figsize=(10, 6))
    plt.bar(words_b, counts_b, color='skyblue')
    plt.title('10 найбільш вживаних слів (ДО очищення)', fontsize=14)
    plt.xlabel('Слово', fontsize=12)
    plt.ylabel('Кількість', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    # 
    plt.show()

    print("\n" + "="*50 + "\n")

    # --- 6. Видалення стоп-слів та пунктуації ---
    print("--- 6. Видалення стоп-слів та пунктуації... ---")
    
    # Отримуємо англійські стоп-слова
    stop_words = set(nltk.corpus.stopwords.words('english'))
    
    # Отримуємо список знаків пунктуації
    punctuation = set(string.punctuation)
    
    # Створюємо новий список "чистих" слів
    cleaned_words = []
    for word in words_lower:
        # Перевіряємо, чи слово є літерним (ігноруємо числа та '--')
        if word.isalpha():
            # Перевіряємо, чи слово НЕ є стоп-словом
            if word not in stop_words:
                cleaned_words.append(word)
                
    new_word_count = len(cleaned_words)
    print(f"Слів після очищення: {new_word_count} (видалено {word_count - new_word_count})")

    # --- 7. 10 найбільш вживаних слів (ПІСЛЯ очищення) ---
    print("\n--- 7. 10 найбільш вживаних слів (ПІСЛЯ очищення) ---")
    
    # Рахуємо частоту "чистих" слів
    freq_dist_after = nltk.FreqDist(cleaned_words)
    
    # Отримуємо 10 найпопулярніших
    most_common_after = freq_dist_after.most_common(10)
    
    for word, count in most_common_after:
        print(f"  {word}: {count} разів")

    # --- 8. Побудова діаграми (після очищення) ---
    # Готуємо дані для графіка
    words_a, counts_a = zip(*most_common_after)
    
    plt.figure(figsize=(10, 6))
    plt.bar(words_a, counts_a, color='salmon')
    plt.title('10 найбільш вживаних слів (ПІСЛЯ очищення)', fontsize=14)
    plt.xlabel('Слово', fontsize=12)
    plt.ylabel('Кількість', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    # 
    plt.show()

except Exception as e:
    print(f"ПОМИЛКА: Не вдалося завантажити або обробити текст.")
    print(f"Деталі помилки: {e}")
    print("Будь ласка, перевірте інтернет-з'єднання та чи правильно вказано ID тексту ('carroll-alice.txt').")
