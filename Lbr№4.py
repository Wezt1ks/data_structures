import time

def count_letters(word):
    counts = {}
    for char in word:
        counts[char] = counts.get(char, 0) + 1
    return counts

def can_make_word_fast(word_counts, available_counts):
    for char, count in word_counts.items():
        if available_counts.get(char, 0) < count:
            return False
    return True

# Инициализация
start_init = time.time()

dictionary_file = 'nouns.txt'

try:
    with open(dictionary_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
except FileNotFoundError:
    print(f"Ошибка: файл '{dictionary_file}' не найден!")
    exit()

dictionary_with_counts = []
for line in lines:
    word = line.strip()
    if word and len(word) > 1:           # исключаем однобуквенные слова
        word_lower = word.lower()
        letter_counts = count_letters(word_lower)
        dictionary_with_counts.append((word_lower, letter_counts))

end_init = time.time()
print(f"Загружено слов: {len(dictionary_with_counts)}")
print(f"Время инициализации: {end_init - start_init:.2f} сек")

# Основной запрос
input_word = input("\nВведите слово: ").strip().lower()

start_process = time.time()
input_counts = count_letters(input_word)

result = []
for dict_word, word_counts in dictionary_with_counts:
    if can_make_word_fast(word_counts, input_counts):
        result.append(dict_word)

result.sort(key=len, reverse=True)
end_process = time.time()

print(f"\nСлова, которые можно составить из '{input_word}':")
for word in result:
    print(f"{word} (длина: {len(word)})")

print(f"\nВсего найдено слов: {len(result)}")
print(f"Время обработки: {end_process - start_process:.4f} сек")
if end_process - start_process > 2.0:
    print("ВНИМАНИЕ: Превышено время (2 сек)!")
else:
    print("Время в норме (≤ 2 сек)")