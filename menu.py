def reset_results():
    pass


def is_data_entered():
    pass


def is_processed():
    pass


def split_text(text):
    pass


def sort_by_length(words):
    pass


def input_manual():
    pass


def input_random():
    pass


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
            print("[ОШИБКА] Некорректный пункт. Введите 0, 1 или 2.")


def process_text():
    pass


def show_result():
    pass


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
            print("[ОШИБКА] Некорректный пункт. Введите 0, 1, 2 или 3.")


if __name__ == "__main__":
    menu_main()