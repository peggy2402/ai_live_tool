# main.py
import os
import sys
import time

# 1. Import tất cả module cần thiết
try:
    from config import VIDEO_OUTPUT_DIR, PLAYLIST_FILE
    from ai_video_generator import AIVideoGenerator
    from live_stream_manager import LiveStreamManager
except ImportError as e:
    print(f"❌ Lỗi import module: {e}")
    print("Đảm bảo các file tồn tại trong cùng thư mục:")
    print("  - config.py")
    print("  - ai_video_generator.py")
    print("  - live_stream_manager.py")
    sys.exit(1)

def main():
    print("=" * 50)
    print("🤖 AI LIVESTREAM TOOL FOR TIKTOK")
    print("=" * 50)
    
    # 2. Khởi tạo các đối tượng
    print("\n1. Đang khởi tạo hệ thống...")
    video_gen = AIVideoGenerator()
    stream_mgr = LiveStreamManager()
    
    # 3. Kiểm tra xem đã có video nào chưa
    print(f"\n2. Kiểm tra thư mục video: {VIDEO_OUTPUT_DIR}")
    if os.path.exists(VIDEO_OUTPUT_DIR):
        videos = [f for f in os.listdir(VIDEO_OUTPUT_DIR) if f.endswith('.mp4')]
        print(f"   Tìm thấy {len(videos)} video")
    
    # 4. Tạo một video mẫu nếu chưa có
    if len(videos) == 0:
        print("\n3. Tạo video mẫu đầu tiên...")
        test_script = "Xin chào! Tôi là AI Avatar. Hãy cùng khám phá sản phẩm mới nào!"
        test_image_url = "https://create-images-results.d-id.com/DefaultPresenters/Willa_f/thumbnail.jpeg"
        
        video_path = video_gen.create_talking_head_video(
            script_text=test_script,
            presenter_image_url=test_image_url,
            output_filename="demo_video"
        )
        
        if video_path:
            print(f"\n✅ Đã tạo video thành công: {video_path}")
            
            # 5. Tạo playlist
            print("\n4. Tạo playlist...")
            stream_mgr.create_looping_playlist([video_path])
        else:
            print("❌ Không thể tạo video. Kiểm tra API Key.")
            return
    
    print("\n🎉 Hệ thống đã sẵn sàng!")
    print("\nCác lệnh tiếp theo:")
    print("  - Chạy 'python main.py' để bắt đầu menu chính")
    print("  - Chỉnh sửa file .env để thay đổi cấu hình")
    print("  - Xem video trong thư mục 'generated_videos'")

if __name__ == "__main__":
    main()