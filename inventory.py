from typing import List, Dict, Optional, Tuple
from storage import load_data, save_data


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
    errors = []
    if not str(data.get("type", "")).strip():
        errors.append("Тип оборудования не может быть пустым")
    if not str(data.get("name", "")).strip():
        errors.append("Наименование не может быть пустым")
    if not str(data.get("cabinet", "")).strip():
        errors.append("Кабинет не может быть пустым")
    if not str(data.get("status", "")).strip():
        errors.append("Состояние не может быть пустым")
    return errors


def add_item(item: Dict) -> Tuple[bool, str]:
    if not str(item.get("inventory_number", "")).strip():
        item["inventory_number"] = generate_inventory_number()

    errors = validate_item(item)
    if errors:
        return False, "Ошибки валидации: " + "; ".join(errors)

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
    """Фильтрация оборудования по состоянию."""
    items = load_inventory()
    status_clean = status.strip().lower()
    return [item for item in items if str(item.get("status", "")).strip().lower() == status_clean]


def update_item(inventory_number: str, updates: Dict) -> Tuple[bool, str]:
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
    cabinet_count = {}

    for item in items:
        status = item.get("status", "не указано")
        cabinet = item.get("cabinet", "не указан")

        status_count[status] = status_count.get(status, 0) + 1
        cabinet_count[cabinet] = cabinet_count.get(cabinet, 0) + 1

    return {
        "total": len(items),
        "by_status": status_count,
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
        for status, count in stats["by_status"].items():
            print(f"  • {status}: {count}")
    else:
        print("  Нет данных")

    print("\nПо кабинетам:")
    if stats["by_cabinet"]:
        for cabinet, count in sorted(stats["by_cabinet"].items()):
            print(f"  • Кабинет {cabinet}: {count}")
    else:
        print("  Нет данных")

    print("=" * 45 + "\n")