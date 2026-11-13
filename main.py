from inventory import (
    show_all_equipment,
    add_item,
    generate_inventory_number,
    search_by_number,
    search_by_cabinet,
    filter_by_status,
    update_item,
    delete_item,
    print_item
)


def show_menu() -> None:
    print("\n" + "=" * 45)
    print("     СИСТЕМА УЧЁТА ИНВЕНТАРЯ")
    print("=" * 45)
    print("1. Показать всё оборудование")
    print("2. Добавить оборудование")
    print("3. Найти по инвентарному номеру")
    print("4. Найти по кабинету")
    print("5. Фильтр по состоянию")
    print("6. Изменить запись")
    print("7. Удалить запись")
    print("8. Выход")
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

    return {
        "inventory_number": inventory_number if inventory_number else generate_inventory_number(),
        "type": type_,
        "name": name,
        "cabinet": cabinet,
        "status": status,
        "date_received": date_received,
        "responsible": responsible
    }


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
            number = input("Введите инвентарный номер: ").strip()
            item = search_by_number(number)
            if item:
                print("\nНайдена запись:")
                print_item(item)
                print()
            else:
                print(f"\nЗапись с номером {number} не найдена.\n")

        elif choice == "4":
            cabinet = input("Введите номер кабинета: ").strip()
            items = search_by_cabinet(cabinet)
            if items:
                print(f"\nНайдено записей в кабинете {cabinet}: {len(items)}\n")
                for item in items:
                    print_item(item)
                print()
            else:
                print(f"\nВ кабинете {cabinet} оборудование не найдено.\n")

        elif choice == "5":
            print("\nДоступные состояния: исправно / требует ремонта / списано")
            status = input("Введите состояние для фильтра: ").strip()
            items = filter_by_status(status)
            if items:
                print(f"\nНайдено записей со статусом «{status}»: {len(items)}\n")
                for item in items:
                    print_item(item)
                print()
            else:
                print(f"\nОборудование со статусом «{status}» не найдено.\n")

        elif choice == "6":
            number = input("Инвентарный номер для изменения: ").strip()
            item = search_by_number(number)
            if not item:
                print(f"\nЗапись с номером {number} не найдена.\n")
                continue

            print("\nТекущая запись:")
            print_item(item)
            print("\nОставьте поле пустым, если не хотите его менять:")

            new_status = input(f"Новое состояние [{item.get('status')}]: ").strip()
            new_cabinet = input(f"Новый кабинет [{item.get('cabinet')}]: ").strip()
            new_responsible = input(f"Новый ответственный [{item.get('responsible')}]: ").strip()

            updates = {}
            if new_status:
                updates["status"] = new_status
            if new_cabinet:
                updates["cabinet"] = new_cabinet
            if new_responsible:
                updates["responsible"] = new_responsible

            if updates:
                success, message = update_item(number, updates)
                print(f"\n{message}\n")
            else:
                print("\nИзменений не внесено.\n")

        elif choice == "7":
            number = input("Инвентарный номер для удаления: ").strip()
            item = search_by_number(number)
            if not item:
                print(f"\nЗапись с номером {number} не найдена.\n")
                continue

            print("\nБудет удалена следующая запись:")
            print_item(item)

            confirm = input("\nПодтвердите удаление (да/нет): ").strip().lower()
            if confirm in ("да", "yes", "y", "д"):
                success, message = delete_item(number)
                print(f"\n{message}\n")
            else:
                print("\nУдаление отменено.\n")

        elif choice == "8":
            print("\nРабота программы завершена. До свидания!")
            break

        else:
            print("\nНеверный выбор. Введите число от 1 до 8.\n")


if __name__ == "__main__":
    main()