
import hashlib

def calculate_blake2b_hash(data):
    blake2_hash = hashlib.blake2b()
    
    blake2_hash.update(data.encode('utf-8'))
    return blake2_hash.hexdigest()

data_to_hash = input("Nhập dữ liệu để hash bằng BLAKE2b: ")
hash_value = calculate_blake2b_hash(data_to_hash)
print("Giá trị hash BLAKE2b:", hash_value)