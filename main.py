from inventory import show_all_equipment, add_item, generate_inventory_number


def show_menu() -> None:
    print("\n" + "=" * 45)
    print("     СИСТЕМА УЧЁТА ИНВЕНТАРЯ")
    print("=" * 45)
    print("1. Показать оборудование")
    print("2. Добавить оборудование")
    print("3. Выход")
    print("=" * 45)


def input_new_item() -> dict:
    print("\n--- Добавление нового оборудования ---")
    print("(оставьте инвентарный номер пустым — он будет сгенерирован автоматически)")

    inventory_number = input("Инвентарный номер: ").strip()
    type_ = input("Тип (ПК / Монитор / Принтер / Проектор и т.д.): ").strip()
    name = input("Наименование: ").strip()
    cabinet = input("Кабинет: ").strip()
    status = input("Состояние (исправно / требует ремонта / списано): ").strip()
    date_received = input("Дата поступления (ГГГГ-ММ-ДД): ").strip()
    responsible = input("Ответственный: ").strip()

    item = {
        "inventory_number": inventory_number if inventory_number else generate_inventory_number(),
        "type": type_,
        "name": name,
        "cabinet": cabinet,
        "status": status,
        "date_received": date_received,
        "responsible": responsible
    }
    return item


def main() -> None:
    while True:
        show_menu()
        choice = input("Выберите пункт меню: ").strip()

        if choice == "1":
            show_all_equipment()

        elif choice == "2":
            item = input_new_item()
            success, message = add_item(item)
            print(f"\n{message}\n")

        elif choice == "3":
            print("\nРабота программы завершена. До свидания!")
            break

        else:
            print("\nНеверный выбор. Введите 1, 2 или 3.\n")


if __name__ == "__main__":
    main()
