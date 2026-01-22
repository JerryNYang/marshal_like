import marshal
import sys

# Detect & Mitigate Marshal Version Mismatch (Prevents Crashes from Old Python 2.x Data)

def safe_marshal_load(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        
        # Detect version mismatch early (marshal.version is 4 in modern Py3)
        if len(data) < 4:
            print("Mitigated: File too short (potential malformed marshal)")
            return None
        
        # Simple heuristic: check magic bytes/header (not foolproof but catches old formats)
        if data[:4] in [b'\x03\xf3\x0d\x0a', b'\x0d\x0a']:  # Old Python 2.x magic examples
            print("Detected vulnerability: Old Python 2.x marshal format - high crash risk")
            print("Mitigated: Rejected load to prevent interpreter corruption")
            return None
        code = marshal.loads(data)
        print("Safe load successful")
        return code

    except ValueError as e:
        print(f"Detected invalid marshal data: {e}")
        print("Mitigated: Caught and rejected")
        return None
    except Exception as e:
        print(f"Unexpected error (possible corruption attempt): {e}")
        return None

# Test in lab: create old marshal file in Py2 VM, try loading here → detects & blocks