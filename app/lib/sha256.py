import hashlib

def sha256(target):
    result = ""
    for key in target.keys():
        result = result + str(key) + str(target[key])
    return hashlib.sha256(result.encode()).hexdigest()
