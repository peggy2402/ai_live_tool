"""
main.py - Giao diện điều khiển chính cho AI Livestream Tool
Tích hợp tất cả tính năng: tạo video, quản lý playlist, stream
"""

import os
import sys
import time
from datetime import datetime

class AILiveStreamApp:
    """Ứng dụng chính điều khiển AI Livestream Tool"""
    
    def __init__(self):
        """Khởi tạo ứng dụng"""
        print("\n" + "="*70)
        print("🤖 AI LIVESTREAM TOOL FOR TIKTOK - BẢN ĐẦY ĐỦ")
        print("="*70)
        print("Phiên bản: 1.0.0 | D-ID API + FFmpeg Stream")
        print("="*70 + "\n")
        
        # Khởi tạo các manager
        self.video_generator = None
        self.stream_manager = None
        self.is_initialized = False
        
        # Khởi tạo hệ thống
        self.initialize_system()
    
    def initialize_system(self):
        """Khởi tạo tất cả các thành phần hệ thống"""
        print("🔧 ĐANG KHỞI TẠO HỆ THỐNG...")
        
        try:
            # 1. Kiểm tra và tải config
            print("   1. 📋 Kiểm tra cấu hình...")
            from config import CONFIG, D_ID_API_KEY
            
            if not CONFIG or not D_ID_API_KEY:
                print("   ❌ Lỗi: Cấu hình không hợp lệ")
                print("   Vui lòng kiểm tra file .env và config.py")
                return False
            
            print(f"      ✅ Config hợp lệ")
            
            # 2. Khởi tạo AI Video Generator
            print("   2. 🎬 Khởi tạo AI Video Generator...")
            from ai_video_generator import AIVideoGenerator
            self.video_generator = AIVideoGenerator()
            
            # Test kết nối API
            print("      🔍 Kiểm tra kết nối D-ID API...")
            if not self.video_generator.test_connection():
                print("      ⚠️  Cảnh báo: Không thể kết nối đến D-ID API")
                print("      Hệ thống vẫn chạy nhưng không thể tạo video mới")
            else:
                print("      ✅ Kết nối API thành công")
            
            # 3. Khởi tạo Live Stream Manager
            print("   3. 📡 Khởi tạo Live Stream Manager...")
            from live_stream_manager import LiveStreamManager
            self.stream_manager = LiveStreamManager()
            
            # 4. Kiểm tra FFmpeg
            print("   4. 🔍 Kiểm tra FFmpeg...")
            if self.check_ffmpeg_installed():
                print("      ✅ FFmpeg đã được cài đặt")
            else:
                print("      ⚠️  Cảnh báo: FFmpeg chưa được cài đặt")
                print("      Tải FFmpeg từ: https://ffmpeg.org/download.html")
                print("      Cần FFmpeg để stream video")
            
            print("\n✅ HỆ THỐNG ĐÃ SẴN SÀNG!")
            print("   📊 Thông tin hệ thống:")
            print(f"      • AI Video Generator: {'✅' if self.video_generator else '❌'}")
            print(f"      • Live Stream Manager: {'✅' if self.stream_manager else '❌'}")
            print(f"      • FFmpeg: {'✅' if self.check_ffmpeg_installed() else '❌'}")
            
            self.is_initialized = True
            return True
            
        except ImportError as e:
            print(f"❌ Lỗi import: {e}")
            print("   Đảm bảo các file sau tồn tại trong cùng thư mục:")
            print("   • config.py")
            print("   • ai_video_generator.py")
            print("   • live_stream_manager.py")
            return False
        except Exception as e:
            print(f"❌ Lỗi khởi tạo hệ thống: {e}")
            return False
    
    def check_ffmpeg_installed(self):
        """Kiểm tra FFmpeg đã được cài đặt chưa"""
        try:
            import subprocess
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def display_main_menu(self):
        """Hiển thị menu chính"""
        print("\n" + "="*70)
        print("📱 MENU CHÍNH - AI LIVESTREAM TOOL")
        print("="*70)
        print("1. 🎬 Tạo video AI mới")
        print("2. 📋 Quản lý playlist")
        print("3. 📡 Bắt đầu livestream")
        print("4. 📊 Xem thống kê hệ thống")
        print("5. ⚙️  Cài đặt & công cụ")
        print("6. 🧪 Chạy thử nghiệm hệ thống")
        print("0. 🚪 Thoát")
        print("="*70)
    
    def create_ai_video(self):
        """Tạo video AI mới"""
        print("\n" + "="*70)
        print("🎬 TẠO VIDEO AI MỚI")
        print("="*70)
        
        if not self.video_generator:
            print("❌ AI Video Generator chưa được khởi tạo")
            return
        
        # Nhập thông tin video
        print("\n📝 NHẬP THÔNG TIN VIDEO:")
        print("-"*50)
        
        # Nhập script
        print("\n1. Nhập kịch bản (tiếng Việt):")
        print("   (Nhập 'DEFAULT' để dùng kịch bản mẫu)")
        script_input = input("   > ").strip()
        
        if script_input.upper() == 'DEFAULT':
            script_text = """
            Xin chào các bạn! Tôi là AI Avatar được tạo bởi công nghệ D-ID.
            Hôm nay tôi sẽ giới thiệu với các bạn những sản phẩm thời trang mới nhất.
            Đây là những chiếc áo len ấm áp, phù hợp với mùa đông lạnh giá.
            Chất liệu mềm mại, thiết kế thời trang, mang lại sự ấm áp và thoải mái.
            Hãy cùng khám phá nhé!
            """
            print(f"   ✅ Đã dùng kịch bản mẫu ({len(script_text)} ký tự)")
        else:
            script_text = script_input
            if len(script_text) < 10:
                print("   ⚠️  Cảnh báo: Script quá ngắn, có thể không tạo được video")
        
        # Nhập URL ảnh
        print("\n2. Nhập URL ảnh khuôn mặt avatar:")
        print("   (Để trống để dùng ảnh mẫu từ D-ID)")
        image_url = input("   > ").strip()
        
        if not image_url:
            image_url = "https://create-images-results.d-id.com/DefaultPresenters/Willa_f/thumbnail.jpeg"
            print(f"   ✅ Đã dùng ảnh mẫu: {image_url[:50]}...")
        elif not image_url.startswith(('http://', 'https://')):
            print("   ❌ URL không hợp lệ, phải bắt đầu với http:// hoặc https://")
            return
        
        # Nhập tên file
        print("\n3. Nhập tên file (không cần .mp4):")
        print("   (Để trống để tự động đặt tên)")
        filename = input("   > ").strip()
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ai_video_{timestamp}"
            print(f"   ✅ Tên file tự động: {filename}")
        
        # Xác nhận tạo video
        print("\n" + "="*50)
        print("📋 XÁC NHẬN THÔNG TIN:")
        print(f"   📝 Script: {len(script_text)} ký tự")
        print(f"   🖼️  Ảnh: {image_url[:60]}...")
        print(f"   📁 Tên file: {filename}.mp4")
        print("="*50)
        
        confirm = input("\n   Bạn có muốn tạo video? (y/n): ").strip().lower()
        
        if confirm != 'y':
            print("   ❌ Đã hủy tạo video")
            return
        
        # Tạo video
        print("\n" + "="*50)
        print("🔄 ĐANG TẠO VIDEO...")
        print("="*50)
        
        video_path = self.video_generator.create_talking_head_video(
            script_text=script_text,
            presenter_image_url=image_url,
            output_filename=filename
        )
        
        if video_path:
            # Tự động thêm video vào playlist
            print("\n➕ ĐANG THÊM VIDEO VÀO PLAYLIST...")
            if self.stream_manager.add_video_to_playlist(video_path):
                print(f"   ✅ Đã thêm vào playlist")
            else:
                print(f"   ⚠️  Không thể thêm vào playlist")
        
        input("\n   Nhấn Enter để tiếp tục...")
    
    def manage_playlist(self):
        """Quản lý playlist"""
        print("\n" + "="*70)
        print("📋 QUẢN LÝ PLAYLIST")
        print("="*70)
        
        if not self.stream_manager:
            print("❌ Live Stream Manager chưa được khởi tạo")
            return
        
        while True:
            print("\n📱 MENU QUẢN LÝ PLAYLIST:")
            print("-"*50)
            print("1. 🔍 Quét thư mục video")
            print("2. 📝 Tạo playlist mới")
            print("3. ➕ Thêm video vào playlist")
            print("4. 📊 Xem thông tin playlist")
            print("5. 🌙 Tạo playlist cho live xuyên đêm")
            print("6. 🧹 Dọn dẹp video cũ")
            print("0. ↩️  Quay lại menu chính")
            print("-"*50)
            
            choice = input("   Lựa chọn của bạn: ").strip()
            
            if choice == '1':
                # Quét thư mục video
                self.stream_manager.scan_video_directory()
                
            elif choice == '2':
                # Tạo playlist mới
                videos = self.stream_manager.scan_video_directory()
                if videos:
                    print("\n🎬 Chọn video cho playlist:")
                    print("   (Nhập số thứ tự video, cách nhau bằng dấu phẩy)")
                    print("   (Để trống để chọn tất cả)")
                    
                    selection = input("   > ").strip()
                    
                    if not selection:
                        # Chọn tất cả
                        selected_videos = videos
                        print(f"   ✅ Đã chọn tất cả {len(videos)} video")
                    else:
                        # Chọn theo số
                        selected_indices = []
                        for part in selection.split(','):
                            part = part.strip()
                            if part.isdigit():
                                idx = int(part) - 1
                                if 0 <= idx < len(videos):
                                    selected_indices.append(idx)
                        
                        if selected_indices:
                            selected_videos = [videos[i] for i in selected_indices]
                            print(f"   ✅ Đã chọn {len(selected_videos)} video")
                        else:
                            print("   ❌ Không có video nào được chọn")
                            continue
                    
                    # Tạo playlist
                    playlist_name = input("   📝 Tên playlist (để trống để dùng mặc định): ").strip()
                    
                    if playlist_name:
                        success = self.stream_manager.create_playlist(selected_videos, playlist_name)
                    else:
                        success = self.stream_manager.create_playlist(selected_videos)
                    
                    if success:
                        print("   ✅ Đã tạo playlist thành công!")
                    else:
                        print("   ❌ Không thể tạo playlist")
                
            elif choice == '3':
                # Thêm video vào playlist
                videos = self.stream_manager.scan_video_directory()
                if videos:
                    print("\n🎬 Chọn video để thêm:")
                    for i, video in enumerate(videos[:20], 1):
                        filename = os.path.basename(video)
                        print(f"   {i:2d}. {filename[:40]:40s}")
                    
                    selection = input("   Số thứ tự video: ").strip()
                    
                    if selection.isdigit():
                        idx = int(selection) - 1
                        if 0 <= idx < len(videos):
                            success = self.stream_manager.add_video_to_playlist(videos[idx])
                            if success:
                                print("   ✅ Đã thêm video vào playlist")
                            else:
                                print("   ❌ Không thể thêm video")
                        else:
                            print("   ❌ Số thứ tự không hợp lệ")
                    else:
                        print("   ❌ Vui lòng nhập số")
                
            elif choice == '4':
                # Xem thông tin playlist
                info = self.stream_manager.get_playlist_info()
                print("\n📊 THÔNG TIN PLAYLIST:")
                print("-"*50)
                print(f"   📋 Tồn tại: {'✅ Có' if info['exists'] else '❌ Không'}")
                print(f"   🎬 Số video: {info['video_count']}")
                print(f"   💾 Kích thước file: {info['file_size']:,} bytes")
                
                if info['videos']:
                    print(f"\n   📁 Danh sách video (10 video đầu):")
                    for i, video in enumerate(info['videos'], 1):
                        filename = os.path.basename(video)
                        print(f"      {i:2d}. {filename[:50]:50s}")
                
            elif choice == '5':
                # Tạo playlist cho live xuyên đêm
                print("\n🌙 TẠO PLAYLIST CHO LIVE XUYÊN ĐÊM")
                print("-"*50)
                
                duration = input("   Số giờ muốn live (mặc định: 8): ").strip()
                if duration.isdigit():
                    duration_hours = int(duration)
                else:
                    duration_hours = 8
                
                print(f"   ⏱️  Đang tạo playlist cho {duration_hours} giờ...")
                self.stream_manager.create_looping_playlist_for_live(duration_hours)
                
            elif choice == '6':
                # Dọn dẹp video cũ
                print("\n🧹 DỌN DẸP VIDEO CŨ")
                print("-"*50)
                
                keep_count = input("   Giữ lại bao nhiêu video gần nhất? (mặc định: 50): ").strip()
                if keep_count.isdigit():
                    keep_n = int(keep_count)
                else:
                    keep_n = 50
                
                confirm = input(f"   Xác nhận xóa video cũ, chỉ giữ {keep_n} video gần nhất? (y/n): ").strip().lower()
                
                if confirm == 'y':
                    deleted, remaining = self.stream_manager.cleanup_old_videos(keep_n)
                    print(f"   ✅ Đã xóa {deleted} video, còn lại {len(remaining)} video")
                else:
                    print("   ❌ Đã hủy")
                
            elif choice == '0':
                # Quay lại menu chính
                break
            
            else:
                print("   ❌ Lựa chọn không hợp lệ")
            
            input("\n   Nhấn Enter để tiếp tục...")
    
    def start_livestream(self):
        """Bắt đầu livestream"""
        print("\n" + "="*70)
        print("📡 BẮT ĐẦU LIVESTREAM")
        print("="*70)
        
        if not self.stream_manager:
            print("❌ Live Stream Manager chưa được khởi tạo")
            return
        
        # Kiểm tra playlist
        playlist_info = self.stream_manager.get_playlist_info()
        if not playlist_info['exists'] or playlist_info['video_count'] == 0:
            print("❌ Playlist trống hoặc không tồn tại")
            print("   Vui lòng tạo playlist trước khi bắt đầu livestream")
            return
        
        # Kiểm tra FFmpeg
        if not self.check_ffmpeg_installed():
            print("❌ FFmpeg chưa được cài đặt")
            print("   Tải FFmpeg từ: https://ffmpeg.org/download.html")
            print("   Sau khi cài đặt, thêm FFmpeg vào PATH và khởi động lại tool")
            return
        
        print(f"\n📊 THÔNG TIN LIVESTREAM:")
        print("-"*50)
        print(f"   📋 Playlist: {playlist_info['file_path']}")
        print(f"   🎬 Số video: {playlist_info['video_count']}")
        print(f"   💾 Kích thước playlist: {playlist_info['file_size']:,} bytes")
        
        print("\n⚙️  CẤU HÌNH STREAM:")
        print("-"*50)
        
        # Chọn virtual camera
        print("   🎥 Chọn virtual camera output:")
        print("   1. OBS Virtual Camera (mặc định)")
        print("   2. DroidCam")
        print("   3. Khác (tự nhập)")
        
        cam_choice = input("   Lựa chọn: ").strip()
        
        if cam_choice == '1':
            virtual_camera = "OBS Virtual Camera"
        elif cam_choice == '2':
            virtual_camera = "DroidCam"
        elif cam_choice == '3':
            virtual_camera = input("   Nhập tên virtual camera: ").strip()
        else:
            virtual_camera = "OBS Virtual Camera"
        
        # Chọn chế độ loop
        loop_choice = input("   🔄 Loop vô hạn? (y/n, mặc định: y): ").strip().lower()
        loop_infinite = loop_choice != 'n'
        
        print("\n" + "="*50)
        print("⚠️  QUAN TRỌNG: HƯỚNG DẪN LIVESTREAM")
        print("="*50)
        print("1. Tool sẽ bắt đầu FFmpeg stream đến virtual camera")
        print("2. Mở OBS Studio và thêm 'Video Capture Device'")
        print("3. Chọn virtual camera vừa tạo làm nguồn")
        print("4. Trên điện thoại, mở TikTok và bắt đầu livestream")
        print("5. Chọn OBS Virtual Camera làm nguồn camera")
        print("6. Đảm bảo tính năng giỏ hàng TikTok Shop được bật")
        print("="*50)
        
        confirm = input("\n   Bạn đã sẵn sàng? (y/n): ").strip().lower()
        
        if confirm != 'y':
            print("   ❌ Đã hủy livestream")
            return
        
        print("\n" + "="*50)
        print("🚀 BẮT ĐẦU LIVESTREAM...")
        print("="*50)
        print("   ⚠️  Lưu ý: Không đóng cửa sổ này khi đang stream")
        print("   Nhấn Ctrl+C để dừng stream khi cần")
        
        # Bắt đầu stream
        success = self.stream_manager.start_ffmpeg_stream(
            virtual_camera=virtual_camera,
            loop_infinite=loop_infinite
        )
        
        if not success:
            print("\n❌ Không thể bắt đầu livestream")
        
        input("\n   Nhấn Enter để tiếp tục...")
    
    def show_system_stats(self):
        """Hiển thị thống kê hệ thống"""
        print("\n" + "="*70)
        print("📊 THỐNG KÊ HỆ THỐNG")
        print("="*70)
        
        # Thông tin hệ thống
        print("\n🔧 THÔNG TIN HỆ THỐNG:")
        print("-"*50)
        print(f"   🐍 Python: {sys.version.split()[0]}")
        print(f"   📁 Thư mục làm việc: {os.getcwd()}")
        print(f"   🕐 Thời gian hệ thống: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Thông tin config
        try:
            from config import CONFIG
            if CONFIG:
                print(f"   ⚙️  Config: ✅ Đã tải")
                print(f"   🔊 Giọng AI: {CONFIG.get('TTS_VOICE_ID', 'N/A')}")
            else:
                print(f"   ⚙️  Config: ❌ Lỗi")
        except:
            print(f"   ⚙️  Config: ❌ Không thể tải")
        
        # Thông tin video generator
        if self.video_generator:
            stats = self.video_generator.get_stats()
            print(f"\n🎬 AI VIDEO GENERATOR:")
            print("-"*50)
            print(f"   📊 Tổng video đã tạo: {stats['total_videos']}")
            print(f"   🔊 Giọng nói: {stats['voice_id']}")
            print(f"   📁 Thư mục lưu: {stats['output_dir']}")
            if stats['last_video']:
                print(f"   🎥 Video cuối cùng: {os.path.basename(stats['last_video'])}")
        else:
            print(f"\n🎬 AI VIDEO GENERATOR: ❌ Chưa khởi tạo")
        
        # Thông tin stream manager
        if self.stream_manager:
            playlist_info = self.stream_manager.get_playlist_info()
            print(f"\n📡 LIVE STREAM MANAGER:")
            print("-"*50)
            print(f"   📋 Playlist: {'✅' if playlist_info['exists'] else '❌'}")
            print(f"   🎬 Số video trong playlist: {playlist_info['video_count']}")
            print(f"   📁 Thư mục video: {self.stream_manager.video_dir}")
        else:
            print(f"\n📡 LIVE STREAM MANAGER: ❌ Chưa khởi tạo")
        
        # Kiểm tra FFmpeg
        print(f"\n🔍 KIỂM TRA CÔNG CỤ:")
        print("-"*50)
        print(f"   📹 FFmpeg: {'✅ Đã cài đặt' if self.check_ffmpeg_installed() else '❌ Chưa cài đặt'}")
        
        input("\n   Nhấn Enter để tiếp tục...")
    
    def settings_and_tools(self):
        """Cài đặt và công cụ"""
        print("\n" + "="*70)
        print("⚙️  CÀI ĐẶT & CÔNG CỤ")
        print("="*70)
        
        while True:
            print("\n📱 MENU CÀI ĐẶT:")
            print("-"*50)
            print("1. 🔑 Kiểm tra API Key")
            print("2. 🌐 Test kết nối internet")
            print("3. 📁 Mở thư mục video")
            print("4. 📄 Xem file log")
            print("5. 🛠️  Sửa lỗi hệ thống")
            print("0. ↩️  Quay lại menu chính")
            print("-"*50)
            
            choice = input("   Lựa chọn của bạn: ").strip()
            
            if choice == '1':
                # Kiểm tra API Key
                print("\n🔑 KIỂM TRA API KEY:")
                print("-"*50)
                try:
                    from config import D_ID_API_KEY
                    if D_ID_API_KEY:
                        key_preview = D_ID_API_KEY[:30] + "..." if len(D_ID_API_KEY) > 30 else D_ID_API_KEY
                        print(f"   ✅ API Key tồn tại")
                        print(f"   📏 Độ dài: {len(D_ID_API_KEY)} ký tự")
                        print(f"   👀 Preview: {key_preview}")
                        
                        # Kiểm tra định dạng
                        if D_ID_API_KEY.startswith('sk_'):
                            print(f"   📝 Định dạng: D-ID Bearer Token (sk_...)")
                        elif ':' in D_ID_API_KEY:
                            print(f"   📝 Định dạng: Username:Password (Basic Auth)")
                        else:
                            print(f"   ⚠️  Định dạng: Không xác định")
                    else:
                        print("   ❌ API Key không tồn tại hoặc rỗng")
                except Exception as e:
                    print(f"   ❌ Lỗi kiểm tra API Key: {e}")
            
            elif choice == '2':
                # Test kết nối internet
                print("\n🌐 KIỂM TRA KẾT NỐI INTERNET:")
                print("-"*50)
                
                import requests
                
                test_urls = [
                    ("Google", "https://www.google.com"),
                    ("D-ID API", "https://api.d-id.com"),
                    ("TikTok", "https://www.tiktok.com")
                ]
                
                for name, url in test_urls:
                    try:
                        start = time.time()
                        response = requests.get(url, timeout=10)
                        latency = (time.time() - start) * 1000
                        
                        if response.status_code == 200:
                            print(f"   ✅ {name}: {latency:.0f}ms")
                        else:
                            print(f"   ⚠️  {name}: {response.status_code} ({latency:.0f}ms)")
                    except requests.exceptions.Timeout:
                        print(f"   ❌ {name}: Timeout")
                    except Exception as e:
                        print(f"   ❌ {name}: {type(e).__name__}")
            
            elif choice == '3':
                # Mở thư mục video
                print("\n📁 MỞ THƯ MỤC VIDEO:")
                print("-"*50)
                
                try:
                    from config import VIDEO_OUTPUT_DIR
                    video_dir = VIDEO_OUTPUT_DIR
                    
                    if os.path.exists(video_dir):
                        print(f"   📂 Thư mục: {video_dir}")
                        
                        # Hiển thị số file
                        mp4_files = [f for f in os.listdir(video_dir) if f.lower().endswith('.mp4')]
                        print(f"   🎬 Số file MP4: {len(mp4_files)}")
                        
                        # Mở thư mục
                        if sys.platform == 'win32':
                            os.system(f'explorer "{os.path.abspath(video_dir)}"')
                        elif sys.platform == 'darwin':
                            os.system(f'open "{os.path.abspath(video_dir)}"')
                        else:
                            os.system(f'xdg-open "{os.path.abspath(video_dir)}"')
                        
                        print(f"   ✅ Đã mở thư mục")
                    else:
                        print(f"   ❌ Thư mục không tồn tại: {video_dir}")
                except Exception as e:
                    print(f"   ❌ Lỗi: {e}")
            
            elif choice == '4':
                # Xem file log (đơn giản)
                print("\n📄 FILE LOG HỆ THỐNG:")
                print("-"*50)
                print("   Tính năng đang phát triển...")
                print("   Logs hiện được hiển thị trực tiếp trên terminal")
            
            elif choice == '5':
                # Sửa lỗi hệ thống
                print("\n🛠️  SỬA LỖI HỆ THỐNG:")
                print("-"*50)
                print("   1. 🔄 Khởi động lại hệ thống")
                print("   2. 🧹 Xóa cache và file tạm")
                print("   3. 📋 Kiểm tra dependencies")
                
                fix_choice = input("   Lựa chọn: ").strip()
                
                if fix_choice == '1':
                    print("   🔄 Đang khởi động lại hệ thống...")
                    self.initialize_system()
                elif fix_choice == '2':
                    print("   Tính năng đang phát triển...")
                elif fix_choice == '3':
                    print("   📦 KIỂM TRA DEPENDENCIES:")
                    print("   -"*25)
                    
                    import pkg_resources
                    required = ['requests', 'python-dotenv']
                    
                    for package in required:
                        try:
                            version = pkg_resources.get_distribution(package).version
                            print(f"   ✅ {package}: {version}")
                        except:
                            print(f"   ❌ {package}: Chưa cài đặt")
            
            elif choice == '0':
                # Quay lại menu chính
                break
            
            else:
                print("   ❌ Lựa chọn không hợp lệ")
            
            input("\n   Nhấn Enter để tiếp tục...")
    
    def run_system_tests(self):
        """Chạy thử nghiệm hệ thống"""
        print("\n" + "="*70)
        print("🧪 CHẠY THỬ NGHIỆM HỆ THỐNG")
        print("="*70)
        
        print("\n🔍 BẮT ĐẦU KIỂM TRA HỆ THỐNG...")
        
        test_results = []
        
        # Test 1: Kiểm tra config
        print("\n1. ⚙️  Kiểm tra config...")
        try:
            from config import CONFIG
            if CONFIG:
                print("   ✅ Config hợp lệ")
                test_results.append(("Config", True))
            else:
                print("   ❌ Config lỗi")
                test_results.append(("Config", False))
        except Exception as e:
            print(f"   ❌ Lỗi config: {e}")
            test_results.append(("Config", False))
        
        # Test 2: Kiểm tra kết nối API
        print("\n2. 🌐 Kiểm tra kết nối D-ID API...")
        if self.video_generator:
            if self.video_generator.test_connection():
                print("   ✅ Kết nối API thành công")
                test_results.append(("API Connection", True))
            else:
                print("   ❌ Không thể kết nối đến API")
                test_results.append(("API Connection", False))
        else:
            print("   ❌ Video Generator chưa khởi tạo")
            test_results.append(("API Connection", False))
        
        # Test 3: Kiểm tra thư mục video
        print("\n3. 📁 Kiểm tra thư mục video...")
        try:
            from config import VIDEO_OUTPUT_DIR
            if os.path.exists(VIDEO_OUTPUT_DIR):
                print(f"   ✅ Thư mục tồn tại: {VIDEO_OUTPUT_DIR}")
                test_results.append(("Video Directory", True))
            else:
                print(f"   ❌ Thư mục không tồn tại")
                test_results.append(("Video Directory", False))
        except Exception as e:
            print(f"   ❌ Lỗi: {e}")
            test_results.append(("Video Directory", False))
        
        # Test 4: Kiểm tra FFmpeg
        print("\n4. 📹 Kiểm tra FFmpeg...")
        if self.check_ffmpeg_installed():
            print("   ✅ FFmpeg đã cài đặt")
            test_results.append(("FFmpeg", True))
        else:
            print("   ❌ FFmpeg chưa cài đặt")
            test_results.append(("FFmpeg", False))
        
        # Test 5: Tạo video test nhỏ
        print("\n5. 🎬 Test tạo video (tùy chọn)...")
        choice = input("   Chạy test tạo video? (y/n): ").strip().lower()
        
        if choice == 'y':
            from ai_video_generator import test_single_video_creation
            result = test_single_video_creation()
            
            if result:
                print("   ✅ Test tạo video thành công")
                test_results.append(("Video Creation", True))
            else:
                print("   ❌ Test tạo video thất bại")
                test_results.append(("Video Creation", False))
        else:
            print("   ⏭️  Bỏ qua test tạo video")
            test_results.append(("Video Creation", "Skipped"))
        
        # Tổng kết test
        print("\n" + "="*50)
        print("📊 KẾT QUẢ KIỂM TRA HỆ THỐNG")
        print("="*50)
        
        passed = sum(1 for _, result in test_results if result is True)
        total = sum(1 for _, result in test_results if result != "Skipped")
        
        for test_name, result in test_results:
            if result is True:
                status = "✅ PASSED"
            elif result is False:
                status = "❌ FAILED"
            else:
                status = "⏭️  SKIPPED"
            print(f"   {test_name:20s} {status}")
        
        print(f"\n   📈 Tổng quan: {passed}/{total} test passed")
        
        if passed == total:
            print("\n   🎉 HỆ THỐNG HOẠT ĐỘNG TỐT!")
        else:
            print("\n   ⚠️  CÓ MỘT SỐ VẤN ĐỀ CẦN SỬA")
            print("   Kiểm tra mục 'Cài đặt & công cụ' để sửa lỗi")
        
        input("\n   Nhấn Enter để tiếp tục...")
    
    def run(self):
        """Chạy ứng dụng chính"""
        if not self.is_initialized:
            print("❌ Hệ thống chưa được khởi tạo thành công")
            print("   Vui lòng kiểm tra file config và thử lại")
            return
        
        while True:
            try:
                self.display_main_menu()
                
                choice = input("   Lựa chọn của bạn: ").strip()
                
                if choice == '1':
                    self.create_ai_video()
                elif choice == '2':
                    self.manage_playlist()
                elif choice == '3':
                    self.start_livestream()
                elif choice == '4':
                    self.show_system_stats()
                elif choice == '5':
                    self.settings_and_tools()
                elif choice == '6':
                    self.run_system_tests()
                elif choice == '0':
                    print("\n👋 Đang thoát...")
                    
                    # Dừng stream nếu đang chạy
                    if self.stream_manager and self.stream_manager.is_streaming:
                        print("   ⏹️  Đang dừng FFmpeg stream...")
                        self.stream_manager.stop_ffmpeg_stream()
                    
                    print("   ✅ Đã thoát AI Livestream Tool")
                    break
                else:
                    print("   ❌ Lựa chọn không hợp lệ")
                    
            except KeyboardInterrupt:
                print("\n\n⚠️  Nhận tín hiệu dừng...")
                
                # Dừng stream nếu đang chạy
                if self.stream_manager and self.stream_manager.is_streaming:
                    print("   ⏹️  Đang dừng FFmpeg stream...")
                    self.stream_manager.stop_ffmpeg_stream()
                
                print("   👋 Tạm biệt!")
                break
            except Exception as e:
                print(f"\n❌ Lỗi không mong đợi: {e}")
                print("   Vui lòng thử lại hoặc khởi động lại tool")
                
                import traceback
                traceback.print_exc()
                
                input("\n   Nhấn Enter để tiếp tục...")


def main():
    """Hàm chính khởi chạy ứng dụng"""
    try:
        app = AILiveStreamApp()
        app.run()
    except Exception as e:
        print(f"\n❌ LỖI NGHIÊM TRỌNG: {e}")
        print("\nNguyên nhân có thể:")
        print("1. Thiếu file cấu hình (.env)")
        print("2. API Key không hợp lệ")
        print("3. Thiếu thư viện cần thiết")
        print("\nCách sửa:")
        print("1. Kiểm tra file .env có tồn tại không")
        print("2. Chạy: pip install -r requirements.txt")
        print("3. Kiểm tra kết nối internet")
        
        input("\nNhấn Enter để thoát...")


if __name__ == "__main__":
    main()