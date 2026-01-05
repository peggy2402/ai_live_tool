# config.py
import os
from dotenv import load_dotenv

# 1. Tải biến môi trường từ file .env
load_dotenv()

# 2. Lấy API Key từ biến môi trường
D_ID_API_KEY = os.getenv('D_ID_API_KEY')

# 3. Kiểm tra nếu không có key
if not D_ID_API_KEY or D_ID_API_KEY == 'your_d_id_api_key_here':
    print("❌ LỖI: Chưa cấu hình API Key!")
    print("Vui lòng:")
    print("  1. Tạo file .env từ .env.example")
    print("  2. Thay thế 'your_d_id_api_key_here' bằng API Key thật của bạn")
    print("  3. Lưu file .env")
    raise ValueError("API Key chưa được cấu hình")

# 4. Các cấu hình khác
D_ID_API_URL = "https://api.d-id.com"
TTS_PROVIDER = os.getenv('TTS_PROVIDER', 'microsoft')
TTS_VOICE_ID = os.getenv('TTS_VOICE_ID', 'vi-VN-HoaiMyNeural')
VIDEO_OUTPUT_DIR = os.getenv('VIDEO_OUTPUT_DIR', 'generated_videos')
PLAYLIST_FILE = os.getenv('PLAYLIST_FILE', 'playlist.txt')

# 5. Tạo thư mục nếu chưa tồn tại
os.makedirs(VIDEO_OUTPUT_DIR, exist_ok=True)

print(f"✅ Đã tải cấu hình từ .env")
print(f"   Thư mục video: {VIDEO_OUTPUT_DIR}")