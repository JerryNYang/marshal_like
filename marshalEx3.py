# Detect Malformed / Corrupted Marshal Data (Buffer Overread Style)

import marshal
import hashlib

def secure_marshal_load_with_hash(file_path, expected_hash = None):
	try:
		with open(file_path, "rb") as f:
			raw = f.read()
		computed = hashlib.sha256(raw).hexdigest()
		if expected_hash and computed != expected_hash:
			print("Detected tampering/corruption: Hash mismatch")
			print("Mitigated: Rejected untrusted marshal data")
			return None

		# Attempt load with size limit to prevent resource exhaustion
		if len(raw) > 1024 * 1024: #1MB cap
			print("Detected vulnerability: Oversized marshal data (DoS risk)")
			return None

		obj = marshal.load(raw)
		print("Secure load ok")
		return obj
	except ValueError:
		print("Detected malformed marshal - possible exploit attempt")
		print("Mitigated: Safe rejection")
		return None

# Lab test: truncate/corrupt a .pyc file → detects malformation, blocks load
