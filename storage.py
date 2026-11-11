import json
from pathlib import Path
from typing import List, Dict


DATA_FILE = Path(__file__).parent / "data" / "inventory.json"


def load_data() -> List[Dict]:
    """
    Загружает данные из JSON.
    - Если файла нет — возвращает пустой список.
    - Если файл повреждён — выводит сообщение и возвращает пустой список.
    """
    try:
        if not DATA_FILE.exists():
            return []
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            if not isinstance(data, list):
                print("Предупреждение: файл inventory.json имеет неверный формат. Загружен пустой список.")
                return []
            return data
    except json.JSONDecodeError:
        print("Ошибка: файл inventory.json повреждён. Загружен пустой список.")
        return []
    except Exception as e:
        print(f"Ошибка чтения файла: {e}")
        return []


def save_data(items: List[Dict]) -> bool:
    """Сохраняет данные в JSON. Возвращает True при успехе."""
    try:
        DATA_FILE.parent.mkdir(exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(items, file, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Ошибка сохранения данных: {e}")
        return False