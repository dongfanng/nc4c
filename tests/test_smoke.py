import importlib


def test_package_importable() -> None:
    importlib.import_module("intellicave")
