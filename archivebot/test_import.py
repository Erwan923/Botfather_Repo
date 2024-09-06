# test_import.py
try:
    from archivebot import db
    print("Import successful")
except ImportError as e:
    print(f"Import failed: {e}")

