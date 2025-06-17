import sys
from PIL import Image

def encode_image(image_path, message):
    """
    Giấu một thông điệp văn bản vào trong một ảnh sử dụng phương pháp LSB.
    """
    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy tệp ảnh tại '{image_path}'")
        return

    width, height = img.size
    
    # 1. Chuyển thông điệp thành chuỗi nhị phân
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    # Thêm một chuỗi ký tự đặc biệt để đánh dấu kết thúc thông điệp
    binary_message += '1111111111111110' 

    # Kiểm tra xem ảnh có đủ lớn để chứa thông điệp không
    if len(binary_message) > width * height * 3:
        print("Lỗi: Thông điệp quá dài để có thể giấu trong ảnh này.")
        return

    data_index = 0
    # 2. Lặp qua từng pixel và giấu từng bit của thông điệp
    for row in range(height):
        for col in range(width):
            # Lấy giá trị pixel (R, G, B)
            pixel = list(img.getpixel((col, row)))

            # Lặp qua 3 kênh màu (Red, Green, Blue)
            for color_channel in range(3):
                # Nếu vẫn còn bit trong thông điệp để giấu
                if data_index < len(binary_message):
                    # Lấy giá trị màu hiện tại, chuyển sang nhị phân,
                    # thay thế bit cuối cùng (LSB) bằng bit của thông điệp
                    original_color_bin = format(pixel[color_channel], '08b')
                    modified_color_bin = original_color_bin[:-1] + binary_message[data_index]
                    
                    # Cập nhật lại giá trị màu cho pixel
                    pixel[color_channel] = int(modified_color_bin, 2)
                    data_index += 1
            
            # Đặt lại pixel đã được sửa đổi vào ảnh
            img.putpixel((col, row), tuple(pixel))

            # Nếu đã giấu xong toàn bộ thông điệp, thoát khỏi các vòng lặp
            if data_index >= len(binary_message):
                # 3. Lưu ảnh mới (chỉ một lần sau khi hoàn thành)
                encoded_image_path = 'encoded_image.png'
                img.save(encoded_image_path)
                print(f"✅ Hoàn thành! Đã giấu thông điệp và lưu ảnh tại: {encoded_image_path}")
                return # Thoát khỏi hàm để không xử lý thêm

def main():
    # Kiểm tra xem người dùng có cung cấp đủ 2 đối số không
    if len(sys.argv) != 3:
        print("Lỗi cú pháp! Cách dùng: python ten_file.py <đường_dẫn_ảnh> \"<thông_điệp>\"")
        print("Ví dụ: python encrypt.py my_image.png \"Hello World\"")
        return

    image_path = sys.argv[1]
    message = sys.argv[2]
    encode_image(image_path, message)

# Điểm bắt đầu chạy chương trình
if __name__ == "__main__":
    main()