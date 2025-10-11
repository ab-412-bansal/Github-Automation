"""
Utility functions for file and directory management.
"""
import os
import json

def ensure_data_dir():
    """Ensure the data directory exists."""
    try:
        if not os.path.exists("data"):
            os.makedirs("data")
    except Exception as e:
        raise RuntimeError(f"Failed to create data directory: {e}")

def save_json(obj, filename):
    """Save a Python object as a JSON file in the data directory."""
    ensure_data_dir()
    path = os.path.join("data", filename)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=2, ensure_ascii=False)
    except Exception as e:
        raise RuntimeError(f"Failed to save JSON to {path}: {e}")
    return path
# src/utils.py
import os
import json

def ensure_data_dir():
    if not os.path.exists("data"):
        os.makedirs("data")

def save_json(obj, filename):
    ensure_data_dir()
    path = os.path.join("data", filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    return path
# src/utils.py
import os
import json

def ensure_data_dir():
    if not os.path.exists("data"):
        os.makedirs("data")

def save_json(obj, filename):
    ensure_data_dir()
    path = os.path.join("data", filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    return path
