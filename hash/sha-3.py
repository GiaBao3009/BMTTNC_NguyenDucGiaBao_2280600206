
import hashlib

def calculate_sha3_256_hash(data):
    # Thay đổi chính nằm ở dòng này
    sha3_hash = hashlib.sha3_256()
    
    sha3_hash.update(data.encode('utf-8'))
    return sha3_hash.hexdigest()

data_to_hash = input("Nhập dữ liệu để hash bằng SHA3-256: ")
hash_value = calculate_sha3_256_hash(data_to_hash)
print("Giá trị hash SHA3-256:", hash_value)