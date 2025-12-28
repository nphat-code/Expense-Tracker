import argparse

# 1. Khởi tạo parser
parser = argparse.ArgumentParser(description="Chương trình chào hỏi người dùng.")

# 2. Khai báo tham số
# Tham số bắt buộc (Positional argument)
parser.add_argument("name", help="Tên của bạn")

# Tham số tùy chọn (Optional argument) có kiểu dữ liệu là số nguyên
parser.add_argument("-c", "--count", type=int, default=1, help="Số lần chào (mặc định là 1)")

# 3. Parse tham số
args = parser.parse_args()

# 4. Sử dụng
for _ in range(args.count):
    print(f"Xin chào, {args.name}!")