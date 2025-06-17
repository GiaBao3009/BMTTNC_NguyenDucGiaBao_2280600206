
import socket
import ssl
import threading

# Thông tin server
server_address = ('localhost', 50000)

# Danh sách các client đã kết nối và Lock để bảo vệ
clients = []
clients_lock = threading.Lock()

def broadcast(message, sender_socket):
    """Gửi thông điệp đến tất cả client khác một cách an toàn."""
    with clients_lock:
        recipients = [client for client in clients if client != sender_socket]

    for client in recipients:
        try:
            client.send(message)
        except:
            remove_client(client)

def remove_client(client_socket):
    """Hàm an toàn để xóa một client."""
    with clients_lock:
        if client_socket in clients:
            clients.remove(client_socket)

def handle_client(client_socket):
    """Hàm xử lý cho mỗi client trong một luồng riêng."""
    with clients_lock:
        clients.append(client_socket)
    print(f"✅ Đã kết nối với: {client_socket.getpeername()}")

    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Nhận từ {client_socket.getpeername()}: {data.decode('utf-8')}")
            broadcast(data, client_socket)
    except Exception as e:
        print(f"Lỗi với {client_socket.getpeername()}: {e}")
    finally:
        print(f"🔌 Đã ngắt kết nối: {client_socket.getpeername()}")
        remove_client(client_socket)
        client_socket.close()

# --- Phần Main của Server ---
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(server_address)
    server_socket.listen(5)
    print(f"🚀 Server đang chờ kết nối tại {server_address}")

    while True:
        client_socket, client_address = server_socket.accept()
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile="./certificates/server-cert.crt",
                                keyfile="./certificates/server-key.key")
        ssl_socket = context.wrap_socket(client_socket, server_side=True)
        client_thread = threading.Thread(target=handle_client, args=(ssl_socket,))
        client_thread.start()
except FileNotFoundError:
    print("\n❌ LỖI: Không tìm thấy tệp chứng chỉ hoặc khóa. Hãy chắc chắn chúng nằm trong thư mục './certificates/'.")
except Exception as e:
    print(f"Lỗi nghiêm trọng của server: {e}")
finally:
    server_socket.close()
    print("Server đã đóng.")