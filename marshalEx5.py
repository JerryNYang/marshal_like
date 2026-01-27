import marshal
import hashlib
import sys

MARSHAL_VERSION = marshal.version  # Pin to current (e.g. 4)

def secure_internal_dump(obj, file_path):
    """Only for trusted internal use - adds version & integrity"""
    data = marshal.dumps(obj)
    version_bytes = MARSHAL_VERSION.to_bytes(1, 'big')
    hash_val = hashlib.sha256(data).digest()
    full = version_bytes + hash_val + data
    
    with open(file_path, "wb") as f:
        f.write(full)
    print("Secure internal marshal dump created")

def secure_internal_load(file_path):
    try:
        with open(file_path, "rb") as f:
            raw = f.read()
        if len(raw) < 33:  # 1 + 32 hash
            raise ValueError("Too short")
        
        ver = int.from_bytes(raw[:1], 'big')
        if ver != MARSHAL_VERSION:
            print("Detected version mismatch - potential old/vuln data")
            return None
        
        stored_hash = raw[1:33]
        data = raw[33:]
        if hashlib.sha256(data).digest() != stored_hash:
            print("Detected tampering")
            return None
        
        obj = marshal.loads(data)
        print("Trusted internal load successful")
        return obj
    except Exception as e:
        print(f"Safe failure: {e}")
        return None

# Lab use: dump/load your own code objects securely → fortifies internal workflows