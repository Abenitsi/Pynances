import hashlib


def create_id(base):
    return hashlib.sha256((str(base).encode("utf-8"))).hexdigest()
