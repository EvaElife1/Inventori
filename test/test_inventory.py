import pytest
from inventory import add_item, find_by_number, load_inventory, save_inventory


@pytest.fixture
def clean_data(tmp_path, monkeypatch):
    """Временный файл данных для тестов."""
    test_file = tmp_path / "inventory.json"
    test_file.write_text("[]", encoding="utf-8")
    monkeypatch.setattr("inventory.DATA_FILE", test_file)
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

    # Пытаемся добавить с тем же номером
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
    assert "Ошибки" in message
