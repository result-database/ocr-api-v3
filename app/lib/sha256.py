import hashlib

def sha256(target):
    return hashlib.sha256(target.encode()).hexdigest()
