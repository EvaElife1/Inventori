from inventory import show_all_equipment


def show_menu() -> None:
    """Показывает главное меню."""
    print("\n" + "=" * 40)
    print("  СИСТЕМА УЧЁТА ИНВЕНТАРЯ")
    print("=" * 40)
    print("1. Показать оборудование")
    print("2. Добавить оборудование (пока заглушка)")
    print("3. Выход")
    print("=" * 40)


def main() -> None:
    """Главный цикл программы."""
    while True:
        show_menu()
        choice = input("Выберите пункт меню: ").strip()

        if choice == "1":
            show_all_equipment()
        elif choice == "2":
            print("\n[Заглушка] Функция добавления будет реализована во 2-м спринте.\n")
        elif choice == "3":
            print("\nРабота программы завершена. До свидания!")
            break
        else:
            print("\nНеверный выбор. Введите 1, 2 или 3.\n")


if __name__ == "__main__":
    main()