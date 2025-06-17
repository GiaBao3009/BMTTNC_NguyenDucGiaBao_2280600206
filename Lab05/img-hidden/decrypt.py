import sys
from PIL import Image

def decode_image(encoded_image_path):
    try:
        img = Image.open(encoded_image_path)
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy tệp ảnh tại '{encoded_image_path}'")
        return None

    width, height = img.size
    binary_message = ""

    # Trích xuất toàn bộ các bit cuối (LSB) từ ảnh
    for row in range(height):
        for col in range(width):
            try:
                pixel = img.getpixel((col, row))
                # Lấy LSB từ 3 kênh màu R, G, B
                for color_channel in range(3):
                    binary_message += format(pixel[color_channel], '08b')[-1]
            except Exception as e:
                # Bỏ qua các pixel có vấn đề (ví dụ: ảnh có kênh Alpha)
                continue

    # --- PHẦN SỬA LỖI LOGIC NẰM Ở ĐÂY ---
    # Tìm đúng dấu hiệu dừng mà encrypt.py đã tạo
    terminator = "1111111111111110"
    terminator_index = binary_message.find(terminator)

    # Nếu không tìm thấy dấu hiệu dừng, có thể có lỗi
    if terminator_index == -1:
        return "LỖI: Không thể tìm thấy dấu hiệu kết thúc thông điệp trong ảnh."

    # Cắt chuỗi nhị phân, chỉ lấy phần chứa thông điệp thực sự
    actual_binary_message = binary_message[:terminator_index]
    
    # Chuyển đổi chuỗi nhị phân thành văn bản
    message = ""
    for i in range(0, len(actual_binary_message), 8):
        byte = actual_binary_message[i:i+8]
        if len(byte) == 8:
            try:
                message += chr(int(byte, 2))
            except ValueError:
                continue
    
    return message

def main():
    if len(sys.argv) != 2:
        print("Usage: python decrypt.py <encoded_image_path>")
        return
    
    encoded_image_path = sys.argv[1]
    decoded_message = decode_image(encoded_image_path)
    
    if decoded_message:
        print("Decoded message:", decoded_message)

if __name__ == "__main__":
    main()