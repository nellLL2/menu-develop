import random
import string
import logging


LOG_LEVEL = logging.INFO


def _make_logger(name, filename, level=None):
    """Создаёт логгер с записью в файл."""
    logger = logging.getLogger(name)
    logger.setLevel(level if level is not None else LOG_LEVEL)
    handler = logging.FileHandler(filename, encoding="utf-8")
    handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))
    logger.addHandler(handler)
    return logger


user_logger = _make_logger("user", "user_actions.log")
server_logger = _make_logger("server", "server_actions.log")
error_logger = _make_logger("error", "errors.log", level=logging.ERROR)


current_text = None
sorted_words = None
is_data_ready = False
is_result_ready = False


def reset_results():
    """Сбрасывает результаты при вводе новых данных."""
    server_logger.info("Вызов: reset_results()")
    global sorted_words, is_data_ready, is_result_ready
    sorted_words = None
    is_data_ready = False
    is_result_ready = False
    print("Предыдущие результаты сброшены.")


def is_data_entered():
    """Проверяет, введены ли исходные данные."""
    server_logger.info("Вызов: is_data_entered()")
    return is_data_ready


def is_processed():
    """Проверяет, выполнен ли алгоритм."""
    server_logger.info("Вызов: is_processed()")
    return is_result_ready


def split_text(text):
    """Разбивает текст на слова по пробелам и знакам препинания."""
    server_logger.info("Вызов: split_text()")
    if text is None or not text.strip():
        raise ValueError("Текст пуст или отсутствует.")
    punctuation = string.punctuation + "«»—–…"
    for ch in punctuation:
        text = text.replace(ch, " ")
    return text.split()


def sort_by_length(words):
    """Сортирует слова по возрастанию длины."""
    server_logger.info("Вызов: sort_by_length()")
    return sorted(words, key=len)


def input_manual():
    """Ручной ввод текста."""
    server_logger.info("Вызов: input_manual()")
    global current_text, is_data_ready
    print("\n--- Ручной ввод текста ---")
    text = input("Введите текст: ").strip()
    if not text:
        raise ValueError("Пользователь ввёл пустую строку.")
    current_text = text
    reset_results()
    is_data_ready = True
    print(f"Текст сохранён ({len(text)} символов).")


def input_random():
    """Генерация случайного текста."""
    server_logger.info("Вызов: input_random()")
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
    """Подменю ввода исходных данных."""
    server_logger.info("Вызов: menu_input()")
    while True:
        print("\n===== ВВОД ДАННЫХ =====")
        print("1) Ввести текст вручную")
        print("2) Сгенерировать случайный текст")
        print("0) Вернуться в главное меню")
        choice = input("Ваш выбор: ").strip()
        user_logger.info(f"Подменю ввода — выбран пункт: {choice}")

        if choice == "1":
            try:
                input_manual()
            except ValueError as e:
                error_logger.error(f"input_manual: {e}")
                print(f"Ошибка: {e}")
        elif choice == "2":
            input_random()
        elif choice == "0":
            return
        else:
            print("Некорректный пункт.")


def process_text():
    """Выполняет алгоритм по заданию."""
    server_logger.info("Вызов: process_text()")
    global sorted_words, is_result_ready
    if not is_data_entered():
        raise RuntimeError("Данные не введены.")
    words = split_text(current_text)
    if not words:
        print("В тексте не найдено слов.")
        sorted_words = []
    else:
        sorted_words = sort_by_length(words)
    is_result_ready = True
    print(f"Алгоритм выполнен. Найдено слов: {len(words)}.")


def show_result():
    """Выводит результат работы алгоритма."""
    server_logger.info("Вызов: show_result()")
    if not is_processed():
        raise RuntimeError("Алгоритм ещё не выполнен.")
    if sorted_words is None:
        raise RuntimeError("Результат отсутствует.")
    if len(sorted_words) == 0:
        print("Массив слов пуст.")
        return
    print("\n========== РЕЗУЛЬТАТ ==========")
    for i, word in enumerate(sorted_words, 1):
        print(f"  {i}. {word} (длина: {len(word)})")
    print(f"\nВсего слов: {len(sorted_words)}")


def menu_main():
    """Главное меню приложения."""
    server_logger.info("Вызов: menu_main()")
    while True:
        print("\n===== СОРТИРОВКА СЛОВ ПО ДЛИНЕ (вариант 12) =====")
        print("1) Ввод исходных данных")
        print("2) Выполнить алгоритм")
        print("3) Вывести результат")
        print("0) Завершить работу")
        choice = input("Ваш выбор: ").strip()
        user_logger.info(f"Главное меню — выбран пункт: {choice}")

        if choice == "1":
            menu_input()
        elif choice == "2":
            try:
                process_text()
            except (RuntimeError, ValueError) as e:
                error_logger.error(f"process_text: {e}")
                print(f"Ошибка: {e}")
        elif choice == "3":
            try:
                show_result()
            except RuntimeError as e:
                error_logger.error(f"show_result: {e}")
                print(f"Ошибка: {e}")
        elif choice == "0":
            print("Завершение работы...")
            break
        else:
            error_logger.error(f"menu_main: некорректный пункт: {choice}")
            print(f"Некорректный пункт: {choice}")


if __name__ == "__main__":
    menu_main()