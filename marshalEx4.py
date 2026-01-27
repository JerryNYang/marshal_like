import marshal
import random

def fuzz_test_marshal_safety(trials=50):
    crashes = 0
    for _ in range(trials):
        # Generate pseudo-random "malicious" bytes
        bad_data = bytes(random.getrandbits(8) for _ in range(random.randint(10, 200)))
        try:
            marshal.loads(bad_data)
        except ValueError:
            pass  # Expected invalid
        except Exception as e:
            print(f"Crash detected on input: {bad_data[:20]!r} → {e}")
            crashes += 1
    
    print(f"Detected {crashes}/{trials} potential crash vectors")
    print("Mitigation recommendation: Never load unvalidated marshal in prod")

# Run this → simulates detecting crash-prone inputs (fortifies by identifying weak points)