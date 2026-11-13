from typing import List, Dict, Optional, Tuple
from storage import load_data, save_data
import re


ALLOWED_STATUSES = {"исправно", "требует ремонта", "списано"}
ALLOWED_TYPES = {
    "пк", "компьютер", "монитор", "принтер", "мфу", "проектор",
    "клавиатура", "мышь", "ноутбук", "роутер", "коммутатор", "сервер"
}


def load_inventory() -> List[Dict]:
    return load_data()


def save_inventory(items: List[Dict]) -> bool:
    return save_data(items)


def get_all_items() -> List[Dict]:
    return load_inventory()


def find_by_number(inventory_number: str) -> Optional[Dict]:
    items = load_inventory()
    for item in items:
        if item.get("inventory_number") == inventory_number:
            return item
    return None


def generate_inventory_number() -> str:
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
    """Строгая проверка данных."""
    errors = []

    type_value = str(data.get("type", "")).strip()
    if not type_value:
        errors.append("Тип оборудования не может быть пустым")
    elif type_value.lower() not in ALLOWED_TYPES and len(type_value) < 2:
        errors.append("Укажите нормальный тип (ПК, Монитор, Принтер, Проектор и т.д.)")

    name = str(data.get("name", "")).strip()
    if not name:
        errors.append("Наименование не может быть пустым")
    elif len(name) < 3:
        errors.append("Наименование слишком короткое (минимум 3 символа)")

    cabinet = str(data.get("cabinet", "")).strip()
    if not cabinet:
        errors.append("Кабинет не может быть пустым")
    elif not re.match(r'^[\w\-а-яА-ЯёЁ]{1,10}$', cabinet):
        errors.append("Кабинет должен быть номером или коротким названием (например 301)")

    status = str(data.get("status", "")).strip().lower()
    if not status:
        errors.append("Состояние не может быть пустым")
    elif status not in ALLOWED_STATUSES:
        errors.append("Состояние должно быть: исправно / требует ремонта / списано")

    date_received = str(data.get("date_received", "")).strip()
    if date_received and not re.match(r'^\d{4}-\d{2}-\d{2}$', date_received):
        errors.append("Дата должна быть в формате ГГГГ-ММ-ДД (например 2024-09-12)")

    responsible = str(data.get("responsible", "")).strip()
    if responsible and len(responsible) < 2:
        errors.append("Имя ответственного слишком короткое")

    return errors


def add_item(item: Dict) -> Tuple[bool, str]:
    if not str(item.get("inventory_number", "")).strip():
        item["inventory_number"] = generate_inventory_number()

    if item.get("status"):
        item["status"] = item["status"].strip().lower()

    errors = validate_item(item)
    if errors:
        return False, "Ошибки валидации:\n- " + "\n- ".join(errors)

    if find_by_number(item["inventory_number"]):
        return False, f"Ошибка: инвентарный номер {item['inventory_number']} уже существует"

    items = load_inventory()
    items.append(item)
    if save_inventory(items):
        return True, f"Оборудование {item['inventory_number']} успешно добавлено"
    return False, "Ошибка при сохранении данных"


def search_by_number(number: str) -> Optional[Dict]:
    return find_by_number(number.strip())


def search_by_cabinet(cabinet: str) -> List[Dict]:
    items = load_inventory()
    return [item for item in items if item.get("cabinet") == cabinet.strip()]


def filter_by_status(status: str) -> List[Dict]:
    items = load_inventory()
    status_clean = status.strip().lower()
    return [item for item in items if str(item.get("status", "")).strip().lower() == status_clean]


def update_item(inventory_number: str, updates: Dict) -> Tuple[bool, str]:
    if "status" in updates:
        status = updates["status"].strip().lower()
        if status not in ALLOWED_STATUSES:
            return False, "Состояние должно быть: исправно / требует ремонта / списано"
        updates["status"] = status

    items = load_inventory()
    for i, item in enumerate(items):
        if item.get("inventory_number") == inventory_number:
            items[i].update(updates)
            if save_inventory(items):
                return True, f"Запись {inventory_number} успешно обновлена"
            return False, "Ошибка при сохранении данных"
    return False, f"Запись с номером {inventory_number} не найдена"


def delete_item(inventory_number: str) -> Tuple[bool, str]:
    items = load_inventory()
    new_items = [item for item in items if item.get("inventory_number") != inventory_number]

    if len(new_items) == len(items):
        return False, f"Запись с номером {inventory_number} не найдена"

    if save_inventory(new_items):
        return True, f"Запись {inventory_number} успешно удалена"
    return False, "Ошибка при сохранении данных"


def print_item(item: Dict) -> None:
    print("-" * 55)
    print(f"  Инв. номер    : {item.get('inventory_number', '—')}")
    print(f"  Тип           : {item.get('type', '—')}")
    print(f"  Наименование  : {item.get('name', '—')}")
    print(f"  Кабинет       : {item.get('cabinet', '—')}")
    print(f"  Состояние     : {item.get('status', '—')}")
    print(f"  Дата пост.    : {item.get('date_received', '—')}")
    print(f"  Ответственный : {item.get('responsible', '—')}")


def show_all_equipment() -> None:
    items = get_all_items()
    if not items:
        print("\nСписок оборудования пуст.\n")
        return
    print(f"\n=== Список оборудования (всего: {len(items)}) ===\n")
    for item in items:
        print_item(item)
    print("-" * 55)
    print()


def get_statistics() -> Dict:
    """Возвращает статистику по состояниям и кабинетам."""
    items = load_inventory()

    status_count = {}
    status_items = {}
    cabinet_count = {}

    for item in items:
        status = item.get("status", "не указано")
        cabinet = item.get("cabinet", "не указан")
        number = item.get("inventory_number", "—")

        status_count[status] = status_count.get(status, 0) + 1
        cabinet_count[cabinet] = cabinet_count.get(cabinet, 0) + 1

        if status not in status_items:
            status_items[status] = []
        status_items[status].append(number)

    return {
        "total": len(items),
        "by_status": status_count,
        "by_status_items": status_items,
        "by_cabinet": cabinet_count
    }


def show_statistics() -> None:
    """Выводит статистику в удобном виде."""
    stats = get_statistics()

    print("\n" + "=" * 45)
    print("           СТАТИСТИКА ОБОРУДОВАНИЯ")
    print("=" * 45)
    print(f"Всего единиц оборудования: {stats['total']}")

    print("\nПо состоянию:")
    if stats["by_status"]:
        order = ["исправно", "требует ремонта", "списано"]
        shown = set()

        for status in order:
            if status in stats["by_status"]:
                count = stats["by_status"][status]
                numbers = stats["by_status_items"].get(status, [])
                print(f"  • {status}: {count}")
                if numbers:
                    print(f"      номера: {', '.join(numbers)}")
                shown.add(status)

        for status, count in stats["by_status"].items():
            if status not in shown:
                numbers = stats["by_status_items"].get(status, [])
                print(f"  • {status}: {count}")
                if numbers:
                    print(f"      номера: {', '.join(numbers)}")
    else:
        print("  Нет данных")

    print("\nПо кабинетам:")
    if stats["by_cabinet"]:
        for cabinet, count in sorted(stats["by_cabinet"].items()):
            print(f"  • Кабинет {cabinet}: {count}")
    else:
        print("  Нет данных")

    print("=" * 45 + "\n")