# tests/test_utils.py
import os
from src.utils import save_json, ensure_data_dir

def test_ensure_data_dir():
    ensure_data_dir()
    assert os.path.exists('data')

def test_save_json():
    test_obj = {'a': 1, 'b': 2}
    filename = 'test_save.json'
    path = save_json(test_obj, filename)
    assert os.path.exists(path)
    with open(path, 'r', encoding='utf-8') as f:
        import json
        data = json.load(f)
    assert data == test_obj
    os.remove(path)
