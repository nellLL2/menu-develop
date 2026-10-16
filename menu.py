import random
import string
import logging


class Messages:
    """Словари текстовых сообщений для локализации."""

    RU = {
        "menu_title": "СОРТИРОВКА СЛОВ ПО ДЛИНЕ (вариант 12)",
        "menu_input": "Ввод исходных данных",
        "menu_process": "Выполнить алгоритм",
        "menu_output": "Вывести результат",
        "menu_exit": "Завершить работу",
        "prompt_choice": "Ваш выбор: ",

        "submenu_title": "ВВОД ДАННЫХ",
        "submenu_manual": "Ввести текст вручную",
        "submenu_random": "Сгенерировать случайный текст",
        "submenu_back": "Вернуться в главное меню",
        "prompt_text": "Введите текст: ",

        "result_title": "РЕЗУЛЬТАТ",
        "result_header": "Слова, отсортированные по возрастанию длины:",
        "result_line": "  {i}. {word} (длина: {length})",
        "result_total": "Всего слов: {n}",

        "ok_text_saved": "Текст сохранён ({n} символов).",
        "ok_random_generated": "Сгенерирован текст ({n} слов):",
        "ok_processed": "Алгоритм выполнен. Найдено слов: {n}.",
        "info_reset": "Предыдущие результаты сброшены.",
        "info_exit": "Завершение работы...",
        "info_interrupt": "Прерывание работы.",
        "warn_no_words": "В тексте не найдено слов.",

        "err_empty_text": "Текст не может быть пустым.",
        "err_no_data": "Данные не введены. Сначала введите данные (пункт 1).",
        "err_no_result": "Результат отсутствует. Сначала выполните алгоритм (пункт 2).",
        "err_invalid_choice": "Некорректный пункт меню: {value}",
        "err_unknown": "Неожиданная ошибка: {value}",
    }

    EN = {
        "menu_title": "SORT WORDS BY LENGTH (variant 12)",
        "menu_input": "Enter source data",
        "menu_process": "Run algorithm",
        "menu_output": "Show result",
        "menu_exit": "Exit",
        "prompt_choice": "Your choice: ",

        "submenu_title": "INPUT DATA",
        "submenu_manual": "Enter text manually",
        "submenu_random": "Generate random text",
        "submenu_back": "Back to main menu",
        "prompt_text": "Enter text: ",

        "result_title": "RESULT",
        "result_header": "Words sorted by length ascending:",
        "result_line": "  {i}. {word} (length: {length})",
        "result_total": "Total words: {n}",

        "ok_text_saved": "Text saved ({n} chars).",
        "ok_random_generated": "Generated text ({n} words):",
        "ok_processed": "Algorithm done. Words found: {n}.",
        "info_reset": "Previous results reset.",
        "info_exit": "Shutting down...",
        "info_interrupt": "Interrupted.",
        "warn_no_words": "No words found in text.",

        "err_empty_text": "Text cannot be empty.",
        "err_no_data": "No data. Enter data first (item 1).",
        "err_no_result": "No result. Run algorithm first (item 2).",
        "err_invalid_choice": "Invalid menu item: {value}",
        "err_unknown": "Unexpected error: {value}",
    }

    _current = RU

    @classmethod
    def set_language(cls, lang):
        if lang == "EN":
            cls._current = cls.EN
        elif lang == "RU":
            cls._current = cls.RU

    @classmethod
    def get(cls, key, **kwargs):
        template = cls._current.get(key, key)
        return template.format(**kwargs) if kwargs else template


def msg(key, **kwargs):
    """Короткий доступ к словарю сообщений."""
    return Messages.get(key, **kwargs)


LOG_LEVEL = logging.INFO


def _make_logger(name, filename, level=None):
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


class AppError(Exception):
    """Базовое исключение приложения. Хранит ключ сообщения."""

    def __init__(self, key, **kwargs):
        self.key = key
        self.kwargs = kwargs
        super().__init__(msg(key, **kwargs))

    def user_message(self):
        return msg(self.key, **self.kwargs)


class NoDataError(AppError):
    """Данные не введены."""

    def __init__(self):
        super().__init__("err_no_data")


class NoResultError(AppError):
    """Результат ещё не получен."""

    def __init__(self):
        super().__init__("err_no_result")


class EmptyTextError(AppError):
    """Пустой текст."""

    def __init__(self):
        super().__init__("err_empty_text")


class InvalidMenuChoiceError(AppError):
    """Некорректный пункт меню."""

    def __init__(self, value):
        super().__init__("err_invalid_choice", value=value)


current_text = None
sorted_words = None
is_data_ready = False
is_result_ready = False


def handle_error(e):
    """Единая точка обработки всех исключений приложения."""
    if isinstance(e, AppError):
        error_logger.error(f"{type(e).__name__}: {e.user_message()}")
        print(e.user_message())
    elif isinstance(e, KeyboardInterrupt):
        error_logger.error("KeyboardInterrupt")
        print(msg("info_interrupt"))
    else:
        error_logger.error(f"Unexpected {type(e).__name__}: {e}")
        print(msg("err_unknown", value=e))


def reset_results():
    server_logger.info("Вызов: reset_results()")
    global sorted_words, is_data_ready, is_result_ready
    sorted_words = None
    is_data_ready = False
    is_result_ready = False
    print(msg("info_reset"))


def is_data_entered():
    server_logger.info("Вызов: is_data_entered()")
    return is_data_ready


def is_processed():
    server_logger.info("Вызов: is_processed()")
    return is_result_ready


def split_text(text):
    server_logger.info("Вызов: split_text()")
    if text is None or not text.strip():
        raise EmptyTextError()
    punctuation = string.punctuation + "«»—–…"
    for ch in punctuation:
        text = text.replace(ch, " ")
    return text.split()


def sort_by_length(words):
    server_logger.info("Вызов: sort_by_length()")
    return sorted(words, key=len)


def input_manual():
    server_logger.info("Вызов: input_manual()")
    global current_text, is_data_ready
    print("\n--- " + msg("submenu_manual") + " ---")
    text = input(msg("prompt_text")).strip()
    if not text:
        raise EmptyTextError()
    current_text = text
    reset_results()
    is_data_ready = True
    print(msg("ok_text_saved", n=len(text)))


def input_random():
    server_logger.info("Вызов: input_random()")
    global current_text, is_data_ready
    print("\n--- " + msg("submenu_random") + " ---")
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
    print(msg("ok_random_generated", n=len(words)))
    print(f"    {text}")


def process_text():
    server_logger.info("Вызов: process_text()")
    global sorted_words, is_result_ready
    if not is_data_entered():
        raise NoDataError()
    words = split_text(current_text)
    if not words:
        print(msg("warn_no_words"))
        sorted_words = []
    else:
        sorted_words = sort_by_length(words)
    is_result_ready = True
    print(msg("ok_processed", n=len(words)))


def show_result():
    server_logger.info("Вызов: show_result()")
    if not is_processed():
        raise NoResultError()
    if sorted_words is None:
        raise NoResultError()
    if len(sorted_words) == 0:
        print(msg("warn_no_words"))
        return
    print(f"\n========== {msg('result_title')} ==========")
    print(msg("result_header"))
    for i, word in enumerate(sorted_words, 1):
        print(msg("result_line", i=i, word=word, length=len(word)))
    print("\n" + msg("result_total", n=len(sorted_words)))


def menu_input():
    server_logger.info("Вызов: menu_input()")
    while True:
        print(f"\n===== {msg('submenu_title')} =====")
        print(f"1) {msg('submenu_manual')}")
        print(f"2) {msg('submenu_random')}")
        print(f"0) {msg('submenu_back')}")
        try:
            choice = input(msg("prompt_choice")).strip()
            user_logger.info(f"Подменю ввода — выбран пункт: {choice}")

            if choice == "1":
                input_manual()
            elif choice == "2":
                input_random()
            elif choice == "0":
                return
            else:
                raise InvalidMenuChoiceError(choice)
        except AppError as e:
            handle_error(e)
        except KeyboardInterrupt:
            handle_error(KeyboardInterrupt())
            return


def menu_main():
    server_logger.info("Вызов: menu_main()")
    while True:
        print(f"\n===== {msg('menu_title')} =====")
        print(f"1) {msg('menu_input')}")
        print(f"2) {msg('menu_process')}")
        print(f"3) {msg('menu_output')}")
        print(f"0) {msg('menu_exit')}")
        try:
            choice = input(msg("prompt_choice")).strip()
            user_logger.info(f"Главное меню — выбран пункт: {choice}")

            if choice == "1":
                menu_input()
            elif choice == "2":
                process_text()
            elif choice == "3":
                show_result()
            elif choice == "0":
                print(msg("info_exit"))
                break
            else:
                raise InvalidMenuChoiceError(choice)
        except AppError as e:
            handle_error(e)
        except KeyboardInterrupt:
            handle_error(KeyboardInterrupt())
            break


if __name__ == "__main__":
    menu_main()