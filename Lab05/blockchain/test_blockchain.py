from blockchain import Blockchain
# Giả sử bạn đã có tệp blockchain.py và block.py hoàn chỉnh

# --- Khởi tạo Blockchain ---
my_blockchain = Blockchain()

def display_chain():
    """Hàm để hiển thị toàn bộ chuỗi blockchain."""
    print("\n----- BẮT ĐẦU HIỂN THỊ BLOCKCHAIN -----")
    if not my_blockchain.chain:
        print("Blockchain hiện đang trống.")
        return
        
    for block in my_blockchain.chain:
        print(f"Block #{block.index}")
        print(f"  Timestamp:     {block.timestamp}")
        # Chuyển đổi list dictionary thành chuỗi dễ đọc hơn
        transactions_str = "\n".join([f"    - Từ: {tx['sender']}, Đến: {tx['receiver']}, Số tiền: {tx['amount']}" for tx in block.transactions])
        if not transactions_str:
            transactions_str = "    - Không có giao dịch nào trong block này."
        print(f"  Transactions:\n{transactions_str}")
        print(f"  Proof:         {block.proof}")
        print(f"  Previous Hash: {block.previous_hash}")
        print(f"  Hash:          {block.hash}")
        print("-----------------------------------------")
    
    # Kiểm tra tính hợp lệ của chuỗi sau khi hiển thị
    is_valid = my_blockchain.is_chain_valid(my_blockchain.chain)
    print(f"✅ Tình trạng Blockchain: {'HỢP LỆ' if is_valid else 'KHÔNG HỢP LỆ'}")
    print("----- KẾT THÚC HIỂN THỊ BLOCKCHAIN -----\n")


# --- Vòng lặp chính của ứng dụng ---
while True:
    print("\n======= MENU CHỨC NĂNG BLOCKCHAIN =======")
    print("1. Thêm một giao dịch mới")
    print("2. Đào một block mới")
    print("3. Hiển thị toàn bộ blockchain")
    print("4. Thoát chương trình")
    
    choice = input("Vui lòng nhập lựa chọn của bạn (1-4): ")

    if choice == '1':
        # --- Thêm giao dịch ---
        print("\n--- Thêm giao dịch mới ---")
        sender = input("Nhập địa chỉ người gửi: ")
        receiver = input("Nhập địa chỉ người nhận: ")
        try:
            amount = float(input("Nhập số tiền: "))
            if amount <= 0:
                print("Lỗi: Số tiền phải là một số dương.")
                continue
            index = my_blockchain.add_transaction(sender, receiver, amount)
            print(f"✅ Giao dịch đã được thêm thành công! Sẽ được đưa vào Block #{index}.")
        except ValueError:
            print("Lỗi: Số tiền không hợp lệ. Vui lòng nhập một con số.")

    elif choice == '2':
        # --- Đào block mới ---
        print("\n--- Bắt đầu đào block mới ---")
        previous_block = my_blockchain.get_previous_block()
        previous_proof = previous_block.proof
        
        print("Đang tìm bằng chứng công việc (Proof of Work)...")
        new_proof = my_blockchain.proof_of_work(previous_proof)
        print(f"Đã tìm thấy bằng chứng: {new_proof}")

        previous_hash = previous_block.hash
        
        # Thưởng cho thợ đào. Địa chỉ '0' ám chỉ đây là một giao dịch mới được tạo ra bởi hệ thống.
        miner_address = input("Nhập địa chỉ của bạn để nhận thưởng đào block: ")
        my_blockchain.add_transaction(sender="0", receiver=miner_address, amount=1)

        # Tạo block mới
        new_block = my_blockchain.create_block(new_proof, previous_hash)
        
        print("\n🎉 CHÚC MỪNG! BẠN ĐÃ ĐÀO THÀNH CÔNG BLOCK MỚI! 🎉")
        print(f"Block #{new_block.index} đã được thêm vào chuỗi.")
        print(f"Hash của block mới: {new_block.hash}")

    elif choice == '3':
        # --- Hiển thị chuỗi ---
        display_chain()

    elif choice == '4':
        # --- Thoát ---
        print("Cảm ơn đã sử dụng chương trình. Tạm biệt!")
        break

    else:
        # --- Lựa chọn không hợp lệ ---
        print("Lỗi: Lựa chọn không hợp lệ. Vui lòng chỉ nhập số từ 1 đến 4.")