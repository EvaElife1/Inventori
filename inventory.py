import json
from pathlib import Path

# Путь к файлу с данными
DATA_FILE = Path(__file__).parent / "data" / "inventory.json"


def load_inventory() -> list[dict]:
    """Загружает список оборудования из JSON-файла."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Ошибка: файл data/inventory.json не найден.")
        return []
    except json.JSONDecodeError:
        print("Ошибка: файл data/inventory.json повреждён.")
        return []


def get_all_items() -> list[dict]:
    """Возвращает весь список оборудования."""
    return load_inventory()


def print_item(item: dict) -> None:
    """Красиво выводит одну запись оборудования."""
    print("-" * 50)
    print(f"  Инв. номер : {item.get('inventory_number', '—')}")
    print(f"  Тип        : {item.get('type', '—')}")
    print(f"  Наименование: {item.get('name', '—')}")
    print(f"  Кабинет    : {item.get('cabinet', '—')}")
    print(f"  Состояние  : {item.get('status', '—')}")
    print(f"  Дата пост. : {item.get('date_received', '—')}")
    print(f"  Ответственный: {item.get('responsible', '—')}")


def show_all_equipment() -> None:
    """Выводит весь список оборудования."""
    items = get_all_items()

    if not items:
        print("\nСписок оборудования пуст.\n")
        return

    print(f"\n=== Список оборудования (всего: {len(items)}) ===\n")
    for item in items:
        print_item(item)
    print("-" * 50)
    print()