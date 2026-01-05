"""
config.py - Cấu hình toàn bộ hệ thống
Xử lý cả API Key dạng 'sk_' và dạng 'username:password' như của bạn
"""

import os
import base64
import sys
from dotenv import load_dotenv

def setup_environment():
    """Thiết lập môi trường và tải biến từ .env"""
    print("🔧 Đang thiết lập môi trường...")
    
    # 1. Tải biến từ file .env
    load_dotenv()
    
    # 2. Đọc API Key từ biến môi trường
    raw_api_key = os.getenv('D_ID_API_KEY', '').strip()
    
    # 3. Kiểm tra và chuẩn hóa API Key
    api_key, auth_header = normalize_api_key(raw_api_key)
    
    # 4. Đọc các cấu hình khác
    config = {
        'API_KEY': api_key,
        'AUTH_HEADER': auth_header,
        'API_URL': "https://api.d-id.com",
        'TTS_PROVIDER': os.getenv('TTS_PROVIDER', 'microsoft'),
        'TTS_VOICE_ID': os.getenv('TTS_VOICE_ID', 'vi-VN-HoaiMyNeural'),
        'VIDEO_OUTPUT_DIR': os.getenv('VIDEO_OUTPUT_DIR', 'generated_videos'),
        'PLAYLIST_FILE': os.getenv('PLAYLIST_FILE', 'playlist.txt'),
        'MAX_RETRIES': int(os.getenv('MAX_RETRIES', '3')),
        'REQUEST_TIMEOUT': int(os.getenv('REQUEST_TIMEOUT', '30'))
    }
    
    # 5. Kiểm tra API Key
    if not config['API_KEY']:
        print("\n❌ LỖI NGHIÊM TRỌNG: API Key không hợp lệ!")
        print("Nguyên nhân có thể:")
        print("   1. File .env không tồn tại hoặc không có D_ID_API_KEY")
        print("   2. API Key bị trống hoặc không đúng định dạng")
        print("\nCách sửa:")
        print("   1. Đảm bảo có file .env trong cùng thư mục")
        print("   2. Kiểm tra API Key trong file .env")
        print("   3. API Key nên bắt đầu bằng 'sk_' hoặc có dạng 'username:password'")
        return None
    
    # 6. Tạo thư mục lưu video nếu chưa tồn tại
    try:
        os.makedirs(config['VIDEO_OUTPUT_DIR'], exist_ok=True)
        print(f"✅ Đã tạo/kiểm tra thư mục: {config['VIDEO_OUTPUT_DIR']}")
    except Exception as e:
        print(f"⚠️  Cảnh báo: Không thể tạo thư mục video: {e}")
        config['VIDEO_OUTPUT_DIR'] = '.'  # Dùng thư mục hiện tại
    
    # 7. Hiển thị thông tin cấu hình (không hiển thị toàn bộ key)
    display_config_summary(config)
    
    return config

def normalize_api_key(raw_key):
    """
    Chuẩn hóa API Key từ nhiều định dạng khác nhau
    Trả về: (api_key, auth_header_value)
    """
    if not raw_key:
        return None, None
    
    # Loại bỏ khoảng trắng thừa
    key = raw_key.strip()
    
    # Định dạng 1: API Key D-ID chuẩn (bắt đầu bằng sk_)
    if key.startswith('sk_'):
        print("✅ Phát hiện API Key D-ID chuẩn (sk_...)")
        return key, f"Bearer {key}"
    
    # Định dạng 2: Dạng username:password (như của bạn)
    if ':' in key and not key.startswith('sk_'):
        print("✅ Phát hiện API Key dạng username:password")
        
        # Mã hóa base64 cho Basic Auth
        try:
            encoded = base64.b64encode(key.encode()).decode()
            return key, f"Basic {encoded}"
        except Exception as e:
            print(f"⚠️  Cảnh báo khi mã hóa API Key: {e}")
            return key, f"Basic {key}"
    
    # Định dạng 3: Đã được mã hóa base64 sẵn
    print("⚠️  API Key không rõ định dạng, thử dùng trực tiếp")
    return key, key

def display_config_summary(config):
    """Hiển thị thông tin cấu hình (ẩn thông tin nhạy cảm)"""
    print("\n" + "="*60)
    print("📋 THÔNG TIN CẤU HÌNH HỆ THỐNG")
    print("="*60)
    
    # Hiển thị API Key (ẩn bớt)
    if config['API_KEY']:
        key_preview = config['API_KEY'][:20] + "..." if len(config['API_KEY']) > 20 else config['API_KEY']
        print(f"   🔑 API Key: {key_preview}")
    
    print(f"   🔊 Giọng nói: {config['TTS_VOICE_ID']}")
    print(f"   📁 Thư mục video: {config['VIDEO_OUTPUT_DIR']}")
    print(f"   📋 File playlist: {config['PLAYLIST_FILE']}")
    print(f"   🔄 Số lần thử lại: {config['MAX_RETRIES']}")
    print(f"   ⏱️  Timeout request: {config['REQUEST_TIMEOUT']}s")
    print("="*60 + "\n")

# Tải cấu hình khi import module
CONFIG = setup_environment()

# Export các biến để các module khác import
if CONFIG:
    D_ID_API_KEY = CONFIG['API_KEY']
    D_ID_AUTH_HEADER = CONFIG['AUTH_HEADER']
    D_ID_API_URL = CONFIG['API_URL']
    TTS_PROVIDER = CONFIG['TTS_PROVIDER']
    TTS_VOICE_ID = CONFIG['TTS_VOICE_ID']
    VIDEO_OUTPUT_DIR = CONFIG['VIDEO_OUTPUT_DIR']
    PLAYLIST_FILE = CONFIG['PLAYLIST_FILE']
    MAX_RETRIES = CONFIG['MAX_RETRIES']
    REQUEST_TIMEOUT = CONFIG['REQUEST_TIMEOUT']
else:
    # Nếu không tải được cấu hình, đặt giá trị mặc định
    D_ID_API_KEY = None
    D_ID_AUTH_HEADER = None
    D_ID_API_URL = "https://api.d-id.com"
    TTS_PROVIDER = "microsoft"
    TTS_VOICE_ID = "vi-VN-HoaiMyNeural"
    VIDEO_OUTPUT_DIR = "generated_videos"
    PLAYLIST_FILE = "playlist.txt"
    MAX_RETRIES = 3
    REQUEST_TIMEOUT = 30
    
    print("⚠️  CẢNH BÁO: Hệ thống chạy với cấu hình mặc định")
    print("   Một số tính năng có thể không hoạt động đúng")

# Test config khi chạy trực tiếp
if __name__ == "__main__":
    print("🧪 Kiểm tra cấu hình...")
    if CONFIG:
        print("✅ Cấu hình hợp lệ!")
    else:
        print("❌ Lỗi cấu hình!")