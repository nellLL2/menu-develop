import random

current_text = None
sorted_words = None
is_data_ready = False
is_result_ready = False


def reset_results():
    global sorted_words, is_data_ready, is_result_ready
    sorted_words = None
    is_data_ready = False
    is_result_ready = False
    print("Предыдущие результаты сброшены.")


def is_data_entered():
    return is_data_ready


def is_processed():
    return is_result_ready


def split_text(text):
    pass


def sort_by_length(words):
    pass


def input_manual():
    global current_text, is_data_ready
    print("\n--- Ручной ввод текста ---")
    text = input("Введите текст: ").strip()
    if not text:
        print("Текст не может быть пустым.")
        return
    current_text = text
    reset_results()
    is_data_ready = True
    print(f"Текст сохранён ({len(text)} символов).")


def input_random():
    global current_text, is_data_ready
    print("\n--- Генерация случайного текста ---")
    word_pool = ["кот", "собака", "я", "привет", "мир", "код",
                 "алгоритм", "данные", "текст", "слово",
                 "длина", "сортировка"]
    count = random.randint(5, 12)
    words = random.choices(word_pool, k=count)
    separators = [", ", ". ", "! ", "? ", " ", "; "]
    text = ""
    for i, w in enumerate(words):
        text += w
        if i < len(words) - 1:
            text += random.choice(separators)
    current_text = text
    reset_results()
    is_data_ready = True
    print(f"Сгенерирован текст ({len(words)} слов):")
    print(f"    {text}")


def menu_input():
    while True:
        print("\n===== ВВОД ДАННЫХ =====")
        print("1) Ввести текст вручную")
        print("2) Сгенерировать случайный текст")
        print("0) Вернуться в главное меню")
        choice = input("Ваш выбор: ").strip()

        if choice == "1":
            input_manual()
        elif choice == "2":
            input_random()
        elif choice == "0":
            return
        else:
            print("Некорректный пункт.")


def process_text():
    if not is_data_entered():
        print("Сначала введите данные (пункт 1).")
        return
    print("Алгоритм ещё не реализован.")


def show_result():
    if not is_processed():
        print("Сначала выполните алгоритм (пункт 2).")
        return
    if sorted_words is None:
        print("Результат отсутствует (алгоритм не реализован).")
        return
    print("\n========== РЕЗУЛЬТАТ ==========")
    for i, word in enumerate(sorted_words, 1):
        print(f"  {i}. {word} (длина: {len(word)})")
    print(f"\nВсего слов: {len(sorted_words)}")


def menu_main():
    while True:
        print("\n===== СОРТИРОВКА СЛОВ ПО ДЛИНЕ (вариант 12) =====")
        print("1) Ввод исходных данных")
        print("2) Выполнить алгоритм")
        print("3) Вывести результат")
        print("0) Завершить работу")
        choice = input("Ваш выбор: ").strip()

        if choice == "1":
            menu_input()
        elif choice == "2":
            process_text()
        elif choice == "3":
            show_result()
        elif choice == "0":
            print("Завершение работы...")
            break
        else:
            print("Некорректный пункт.")


if __name__ == "__main__":
    menu_main()