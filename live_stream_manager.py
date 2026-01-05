# live_stream_manager.py
import subprocess
import os
import sys

# Import từ config.py
try:
    from config import PLAYLIST_FILE, VIDEO_OUTPUT_DIR
except ImportError:
    print("❌ Không tìm thấy config.py")
    sys.exit(1)

class LiveStreamManager:
    def __init__(self):
        # Sử dụng biến từ config
        self.playlist_path = PLAYLIST_FILE
        self.video_dir = VIDEO_OUTPUT_DIR
        
        print(f"✅ Khởi tạo LiveStreamManager")
        print(f"   Playlist: {self.playlist_path}")
        print(f"   Thư mục video: {self.video_dir}")
    
    # ... (các phương thức khác giữ nguyên)