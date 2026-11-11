import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from inventory import (
    add_item,
    find_by_number,
    search_by_number,
    search_by_cabinet,
    update_item,
    delete_item,
    generate_inventory_number,
    validate_item
)


@pytest.fixture
def clean_data(tmp_path, monkeypatch):
    """Создаёт временный чистый файл данных для каждого теста."""
    test_file = tmp_path / "inventory.json"
    test_file.write_text("[]", encoding="utf-8")
    # Патчим DATA_FILE в модуле storage, а не inventory
    monkeypatch.setattr("storage.DATA_FILE", test_file)
    return test_file


def test_add_item_success(clean_data):
    item = {
        "inventory_number": "INV-100",
        "type": "ПК",
        "name": "Тестовый компьютер",
        "cabinet": "101",
        "status": "исправно",
        "date_received": "2025-01-01",
        "responsible": "Тестов Т.Т."
    }
    success, message = add_item(item)
    assert success is True
    assert "успешно добавлено" in message
    assert find_by_number("INV-100") is not None


def test_add_item_duplicate_number(clean_data):
    item = {
        "inventory_number": "INV-100",
        "type": "ПК",
        "name": "Компьютер 1",
        "cabinet": "101",
        "status": "исправно",
        "date_received": "2025-01-01",
        "responsible": "Тестов"
    }
    add_item(item)
    success, message = add_item(item)
    assert success is False
    assert "уже существует" in message


def test_add_item_empty_fields(clean_data):
    item = {
        "inventory_number": "INV-101",
        "type": "",
        "name": "",
        "cabinet": "101",
        "status": "исправно",
        "date_received": "",
        "responsible": ""
    }
    success, message = add_item(item)
    assert success is False
    assert "Ошибки валидации" in message


def test_search_existing_number(clean_data):
    item = {
        "inventory_number": "INV-100",
        "type": "ПК",
        "name": "Тестовый ПК",
        "cabinet": "301",
        "status": "исправно",
        "date_received": "2025-01-01",
        "responsible": "Тестов"
    }
    add_item(item)
    result = search_by_number("INV-100")
    assert result is not None
    assert result["name"] == "Тестовый ПК"


def test_search_non_existing_number(clean_data):
    result = search_by_number("INV-999")
    assert result is None


def test_search_by_cabinet(clean_data):
    item1 = {
        "inventory_number": "INV-101",
        "type": "Монитор",
        "name": "Монитор 1",
        "cabinet": "205",
        "status": "исправно",
        "date_received": "2025-01-01",
        "responsible": "Тестов"
    }
    item2 = {
        "inventory_number": "INV-102",
        "type": "ПК",
        "name": "ПК 1",
        "cabinet": "205",
        "status": "исправно",
        "date_received": "2025-01-01",
        "responsible": "Тестов"
    }
    add_item(item1)
    add_item(item2)
    results = search_by_cabinet("205")
    assert len(results) == 2


def test_search_by_cabinet_empty(clean_data):
    results = search_by_cabinet("999")
    assert results == []


def test_update_existing_item(clean_data):
    item = {
        "inventory_number": "INV-200",
        "type": "ПК",
        "name": "Старый ПК",
        "cabinet": "101",
        "status": "исправно",
        "date_received": "2025-01-01",
        "responsible": "Тестов"
    }
    add_item(item)
    success, message = update_item("INV-200", {"status": "требует ремонта", "cabinet": "202"})
    assert success is True
    assert "успешно обновлена" in message
    updated = find_by_number("INV-200")
    assert updated["status"] == "требует ремонта"
    assert updated["cabinet"] == "202"


def test_update_non_existing_item(clean_data):
    success, message = update_item("INV-999", {"status": "списано"})
    assert success is False
    assert "не найдена" in message


def test_delete_existing_item(clean_data):
    item = {
        "inventory_number": "INV-300",
        "type": "Принтер",
        "name": "Принтер HP",
        "cabinet": "101",
        "status": "исправно",
        "date_received": "2025-01-01",
        "responsible": "Тестов"
    }
    add_item(item)
    success, message = delete_item("INV-300")
    assert success is True
    assert "успешно удалена" in message
    assert find_by_number("INV-300") is None


def test_delete_non_existing_item(clean_data):
    success, message = delete_item("INV-999")
    assert success is False
    assert "не найдена" in message