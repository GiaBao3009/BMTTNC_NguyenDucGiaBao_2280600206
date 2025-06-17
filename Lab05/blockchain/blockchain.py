from block import Block
import hashlib
import time
import json # Thêm json để có thể hash dictionary

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        # Tạo khối nguyên thủy (genesis block)
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        """
        Tạo một khối mới và thêm vào chuỗi
        """
        # Lớp Block cần được định nghĩa trong tệp block.py
        block = Block(
            index=len(self.chain) + 1,
            previous_hash=previous_hash,
            timestamp=time.time(),
            transactions=self.current_transactions,
            proof=proof
        )
        # Reset danh sách giao dịch hiện tại
        self.current_transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        """
        Lấy khối cuối cùng trong chuỗi
        """
        return self.chain[-1]

    def add_transaction(self, sender, receiver, amount):
        """
        Thêm một giao dịch mới vào danh sách giao dịch chờ
        """
        self.current_transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })
        # Trả về chỉ số của khối sẽ chứa giao dịch này
        return self.get_previous_block().index + 1

    def proof_of_work(self, previous_proof):
        """
        Thuật toán Bằng chứng Công việc đơn giản:
        - Tìm một số 'new_proof' sao cho hash(new_proof^2 - previous_proof^2) có 4 số 0 ở đầu
        """
        new_proof = 1
        check_proof = False
        while not check_proof:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation.startswith('0000'):
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def is_chain_valid(self, chain):
        """
        Kiểm tra xem toàn bộ blockchain có hợp lệ không
        """
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            # 1. Kiểm tra liên kết hash
            if block.previous_hash != previous_block.hash:
                return False

            # 2. Kiểm tra bằng chứng công việc
            previous_proof = previous_block.proof
            proof = block.proof
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if not hash_operation.startswith('0000'):
                return False
            
            previous_block = block
            block_index += 1
        return True