# client.py
import socket
import ssl
import threading

# Thông tin server (phải khớp với server.py)
server_address = ('localhost', 50000)

def receive_data(ssl_socket):
    """Hàm chạy trong luồng riêng để liên tục nhận dữ liệu từ server."""
    while True:
        try:
            data = ssl_socket.recv(1024)
            if not data:
                print("\nServer đã đóng kết nối.")
                break
            # Dùng \r để xóa dòng input hiện tại trước khi in tin nhắn mới
            print(f"\r[Người khác]: {data.decode('utf-8')}\nBạn: ", end="")
        except:
            break

# --- Phần Main của Client ---
try:
    # Tạo socket client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Tạo SSL context chính xác cho client
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    # Vì dùng chứng chỉ tự ký nên ta không xác thực phía client
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    # Bọc socket trong SSL và kết nối
    ssl_socket = context.wrap_socket(client_socket, server_hostname='localhost')
    ssl_socket.connect(server_address)
    print("✅ Đã kết nối đến server. Có thể bắt đầu chat.")
    print("Gõ 'quit' để thoát.")

    # Bắt đầu một luồng để nhận dữ liệu từ server
    receive_thread = threading.Thread(target=receive_data, args=(ssl_socket,), daemon=True)
    receive_thread.start()

    # Vòng lặp ở luồng chính để gửi dữ liệu
    while True:
        message = input("Bạn: ")
        if message.lower() == 'quit':
            break
        if message:
            ssl_socket.send(message.encode('utf-8'))
            
except ConnectionRefusedError:
    print("❌ LỖI: Kết nối bị từ chối. Server có đang chạy không?")
except Exception as e:
    print(f"Đã xảy ra lỗi: {e}")
finally:
    print("🔌 Đang đóng kết nối...")
    ssl_socket.close()