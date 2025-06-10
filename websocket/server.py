import random
import tornado.ioloop
import tornado.web
import tornado.websocket

class WebSocketServer(tornado.websocket.WebSocketHandler):
    # Dùng một set ở cấp độ class để lưu tất cả các kết nối client
    clients = set()

    def open(self):
        """Được gọi khi một client mới kết nối."""
        print("New client connected")
        WebSocketServer.clients.add(self)

    def on_close(self):
        """Được gọi khi một client ngắt kết nối."""
        print("Client disconnected")
        WebSocketServer.clients.remove(self)

    @classmethod
    def send_message(cls, message: str):
        """Gửi một tin nhắn đến tất cả các client đang kết nối."""
        print(f"Sending message '{message}' to {len(cls.clients)} client(s).")
        for client in cls.clients:
            try:
                client.write_message(message)
            except tornado.websocket.WebSocketClosedError:
                print("Failed to send to a closed client.")
                # Có thể xóa client ở đây nếu cần, nhưng on_close sẽ xử lý
                pass

class RandomWordSelector:
    """Một lớp đơn giản để chọn một từ ngẫu nhiên từ danh sách."""
    def __init__(self, word_list):
        self.word_list = word_list

    def sample(self):
        """Trả về một từ ngẫu nhiên."""
        return random.choice(self.word_list)

def main():
    """Hàm chính để thiết lập và chạy server."""
    app = tornado.web.Application([
        (r"/websocket/", WebSocketServer),
    ],
    # Cấu hình để giữ kết nối WebSocket ổn định
    websocket_ping_interval=10,
    websocket_ping_timeout=30,
    )
    
    port = 8888
    app.listen(port)
    print(f"Server is running on ws://localhost:{port}/websocket/")

    # Lấy vòng lặp I/O hiện tại
    io_loop = tornado.ioloop.IOLoop.current()

    # Tạo một đối tượng để chọn từ ngẫu nhiên
    word_selector = RandomWordSelector(['apple', 'banana', 'orange', 'grape', 'melon', 'strawberry'])

    # Thiết lập một callback định kỳ để gửi từ sau mỗi 3 giây (3000ms)
    periodic_callback = tornado.ioloop.PeriodicCallback(
        lambda: WebSocketServer.send_message(word_selector.sample()), 3000
    )
    periodic_callback.start()

    # Bắt đầu vòng lặp sự kiện của server
    io_loop.start()


if __name__ == "__main__":
    main()

