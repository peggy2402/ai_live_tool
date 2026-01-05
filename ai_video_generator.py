# ai_video_generator.py
import requests
import time
import os
import sys

# CÁCH 1: Import từ config.py (khuyến nghị)
try:
    from config import D_ID_API_KEY, D_ID_API_URL, TTS_PROVIDER, TTS_VOICE_ID, VIDEO_OUTPUT_DIR
    print("✅ Đã import cấu hình từ config.py")
except ImportError as e:
    print(f"❌ Lỗi import config: {e}")
    print("Đảm bảo file config.py tồn tại trong cùng thư mục")
    sys.exit(1)

class AIVideoGenerator:
    def __init__(self):
        # Sử dụng biến đã import từ config
        self.api_key = D_ID_API_KEY
        self.api_url = D_ID_API_URL
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Kiểm tra API Key
        if not self.api_key or "your_d_id_api_key" in self.api_key:
            print("⚠️  CẢNH BÁO: API Key chưa được cấu hình đúng!")
            print("   Vui lòng kiểm tra file .env")
            return None
            
        print(f"✅ Khởi tạo AIVideoGenerator thành công")
        print(f"   Giọng nói: {TTS_VOICE_ID}")
        
    # ... (các phương thức khác giữ nguyên)