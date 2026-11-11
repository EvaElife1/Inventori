import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from storage import load_data, save_data


@pytest.fixture
def temp_data_file(tmp_path, monkeypatch):
    test_file = tmp_path / "inventory.json"
    monkeypatch.setattr("storage.DATA_FILE", test_file)
    return test_file


def test_load_missing_file(temp_data_file):
    """Отсутствие файла возвращает пустой список."""
    assert not temp_data_file.exists()
    data = load_data()
    assert data == []


def test_save_and_load(temp_data_file):
    """Данные корректно сохраняются и загружаются."""
    items = [
        {
            "inventory_number": "INV-001",
            "type": "ПК",
            "name": "Тест",
            "cabinet": "101",
            "status": "исправно",
            "date_received": "2025-01-01",
            "responsible": "Тест"
        }
    ]
    assert save_data(items) is True
    loaded = load_data()
    assert len(loaded) == 1
    assert loaded[0]["inventory_number"] == "INV-001"


def test_load_corrupted_json(temp_data_file):
    """Повреждённый JSON возвращает пустой список."""
    temp_data_file.write_text("{это не json", encoding="utf-8")
    data = load_data()
    assert data == []


def test_load_invalid_format(temp_data_file):
    """Файл с не-списком возвращает пустой список."""
    temp_data_file.write_text('{"key": "value"}', encoding="utf-8")
    data = load_data()
    assert data == []