from input import hash_code
import hashlib

def test_valid():
    assert hash_code("1") == hashlib.sha256("1".encode("utf-8")).hexdigest()
    assert hash_code("cs50") == hashlib.sha256("cs50".encode("utf-8")).hexdigest()
    assert hash_code("investor") == hashlib.sha256("investor".encode("utf-8")).hexdigest()
