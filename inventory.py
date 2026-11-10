import json
from pathlib import Path
from typing import List, Dict, Optional

DATA_FILE = Path(__file__).parent / "data" / "inventory.json"


def load_inventory() -> List[Dict]:
    """Загружает список оборудования из JSON."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_inventory(items: List[Dict]) -> None:
    """Сохраняет список оборудования в JSON."""
    DATA_FILE.parent.mkdir(exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def get_all_items() -> List[Dict]:
    return load_inventory()


def find_by_number(inventory_number: str) -> Optional[Dict]:
    """Ищет запись по инвентарному номеру."""
    items = load_inventory()
    for item in items:
        if item.get("inventory_number") == inventory_number:
            return item
    return None


def generate_inventory_number() -> str:
    """Генерирует следующий инвентарный номер вида INV-XXX."""
    items = load_inventory()
    max_num = 0
    for item in items:
        num_str = item.get("inventory_number", "INV-000")
        try:
            num = int(num_str.split("-")[1])
            if num > max_num:
                max_num = num
        except (IndexError, ValueError):
            continue
    return f"INV-{max_num + 1:03d}"


def validate_item(data: Dict) -> List[str]:
    """Проверяет данные. Возвращает список ошибок."""
    errors = []
    if not data.get("type", "").strip():
        errors.append("Тип оборудования не может быть пустым")
    if not data.get("name", "").strip():
        errors.append("Наименование не может быть пустым")
    if not data.get("cabinet", "").strip():
        errors.append("Кабинет не может быть пустым")
    if not data.get("status", "").strip():
        errors.append("Состояние не может быть пустым")
    return errors


def add_item(item: Dict) -> tuple[bool, str]:
    """Добавляет новую запись. Возвращает (успех, сообщение)."""
    errors = validate_item(item)
    if errors:
        return False, "Ошибки: " + "; ".join(errors)

    if not item.get("inventory_number"):
        item["inventory_number"] = generate_inventory_number()

    if find_by_number(item["inventory_number"]):
        return False, f"Ошибка: номер {item['inventory_number']} уже существует"

    items = load_inventory()
    items.append(item)
    save_inventory(items)
    return True, f"Оборудование {item['inventory_number']} успешно добавлено"


def search_by_number(number: str) -> Optional[Dict]:
    """Поиск по инвентарному номеру."""
    return find_by_number(number.strip())


def search_by_cabinet(cabinet: str) -> List[Dict]:
    """Поиск всех записей по кабинету."""
    items = load_inventory()
    return [item for item in items if item.get("cabinet") == cabinet.strip()]


def update_item(inventory_number: str, updates: Dict) -> tuple[bool, str]:
    """Изменение записи."""
    items = load_inventory()
    for i, item in enumerate(items):
        if item.get("inventory_number") == inventory_number:
            items[i].update(updates)
            save_inventory(items)
            return True, f"Запись {inventory_number} успешно обновлена"
    return False, f"Запись с номером {inventory_number} не найдена"


def delete_item(inventory_number: str) -> tuple[bool, str]:
    """Удаление записи."""
    items = load_inventory()
    new_items = [item for item in items if item.get("inventory_number") != inventory_number]

    if len(new_items) == len(items):
        return False, f"Запись с номером {inventory_number} не найдена"

    save_inventory(new_items)
    return True, f"Запись {inventory_number} успешно удалена"


def print_item(item: Dict) -> None:
    """Красиво выводит одну запись."""
    print("-" * 50)
    print(f"  Инв. номер   : {item.get('inventory_number', '—')}")
    print(f"  Тип          : {item.get('type', '—')}")
    print(f"  Наименование : {item.get('name', '—')}")
    print(f"  Кабинет      : {item.get('cabinet', '—')}")
    print(f"  Состояние    : {item.get('status', '—')}")
    print(f"  Дата пост.   : {item.get('date_received', '—')}")
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
    print("-" * 50 + "\n")