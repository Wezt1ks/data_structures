import docx
import time
import sys
import os

def contains(main_str, sub_str):
    #Ручная проверка подстроки
    len_sub = len(sub_str)
    len_main = len(main_str)
    for i in range(len_main - len_sub + 1):
        if main_str[i:i+len_sub] == sub_str:
            return True
    return False

def is_letter(ch):
    #Буква (русская, латинская, ё).
    if 'a' <= ch <= 'z' or 'A' <= ch <= 'Z':
        return True
    if 'а' <= ch <= 'я' or 'А' <= ch <= 'Я' or ch in 'ёЁ':
        return True
    french_letters = (
        'àâçéèêëîïôûùüÿœæ'
        'ÀÂÇÉÈÊËÎÏÔÛÙÜŸŒÆ'
    )
    if ch in french_letters:
        return True
    return False

def find_docx_file():
    #Ищет файл .docx сначала в папке скрипта, затем в текущей рабочей папке.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    possible_paths = [
        os.path.join(script_dir, 'voina-i-mir.docx'),
        os.path.join(script_dir, 'Война и мир.docx'),
        'voina-i-mir.docx',
        'Война и мир.docx'
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def extract_words_from_docx(filepath):
    #Извлекает слова из .docx, возвращает список всех слов.
    print(f"Загрузка файла: {filepath}")
    start_time = time.time()

    try:
        doc = docx.Document(filepath)
    except Exception as e:
        print(f" Ошибка при чтении файла: {e}")
        print(f" Текущая рабочая папка: {os.getcwd()}")
        print(f" Папка со скриптом: {os.path.dirname(os.path.abspath(__file__))}")
        sys.exit(1)

    full_text = []
    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            full_text.append(paragraph.text)
    text = ' '.join(full_text)
    print(f"Размер текста: {len(text)} символов")

    words = []
    current_word = []
    for ch in text:
        if is_letter(ch):
            current_word.append(ch.lower())
        else:
            if current_word:
                words.append(''.join(current_word))
                current_word = []
    if current_word:
        words.append(''.join(current_word))

    print(f"Всего слов найдено: {len(words)}")
    processing_time = time.time() - start_time
    print(f" Текст обработан за {processing_time:.2f} сек\n")
    return words

def calculate_frequencies(words):
    #Возвращает (unique_words, frequencies) без словарей.
    if not words:
        return [], []
    words_sorted = sorted(words)
    unique = []
    freqs = []
    prev = words_sorted[0]
    count = 1
    for w in words_sorted[1:]:
        if w == prev:
            count += 1
        else:
            unique.append(prev)
            freqs.append(count)
            prev = w
            count = 1
    unique.append(prev)
    freqs.append(count)
    return unique, freqs

def search(query, unique_words, frequencies, max_results=20):
    if len(query) < 3:
        print("Запрос должен содержать не менее 3 символов!")
        return []
    query = query.lower().strip()
    start_time = time.time()

    matched = []
    for i, word in enumerate(unique_words):
        if contains(word, query):
            matched.append((word, frequencies[i]))

    matched.sort(key=lambda x: x[1], reverse=True)
    results = matched[:max_results]

    print(f"Поиск выполнен за {time.time() - start_time:.4f} сек")
    return results

def display_results(results, query):
    print(f"\n{'='*60}")
    print(f"Результаты поиска по запросу: '{query}'")
    print(f"Найдено слов: {len(results)}")
    print('='*60)
    if not results:
        print("Слова не найдены")
        print('='*60 + "\n")
        return
    print(f"{'№':<3} {'Слово':<35} {'Частота':>10}")
    print('-'*60)
    for i, (word, freq) in enumerate(results, 1):
        print(f"{i:<3} {word:<35} {freq:>10}")
    print('='*60 + "\n")

def main():
    print("\n   ПОИСК ПО ТЕКСТУ РОМАНА «ВОЙНА И МИР»")
    print("   (Л.Н. Толстой)")
    print("\nПрограмма находит слова, содержащие введённую подстроку.")
    print("Результаты сортируются по частоте встречаемости в тексте.")
    print("Минимальная длина запроса: 3 символа")
    print("Для выхода введите: quit или exit"+ "\n")

    # Автоматический поиск файла
    docx_path = find_docx_file()
    if not docx_path:
        print(" Файл 'voina-i-mir.docx' не найден!")
        print(f"  Текущая рабочая папка: {os.getcwd()}")
        print(f"  Папка со скриптом: {os.path.dirname(os.path.abspath(__file__))}")
        print("\n  Положите файл в одну из этих папок и перезапустите программу.")
        sys.exit(1)

    all_words = extract_words_from_docx(docx_path)
    unique_words, frequencies = calculate_frequencies(all_words)

    while True:
        try:
            query = input("Введите запрос для поиска: ").strip()
            if query.lower() in ('quit', 'exit', 'выход'):
                print("\nПрограмма завершена.")
                break
            results = search(query, unique_words, frequencies)
            display_results(results, query)
        except KeyboardInterrupt:
            print("\n\nПрограмма завершена пользователем.")
            break
        except Exception as e:
            print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()