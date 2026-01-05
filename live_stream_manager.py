"""
live_stream_manager.py - Quản lý playlist và stream video
Hỗ trợ tạo playlist cho FFmpeg, quản lý danh sách video, và stream liên tục
"""

import os
import subprocess
import time
import json
import sys
from datetime import datetime

class LiveStreamManager:
    """
    Quản lý playlist video và stream cho AI Livestream
    """
    
    def __init__(self):
        """Khởi tạo stream manager"""
        try:
            from config import VIDEO_OUTPUT_DIR, PLAYLIST_FILE
            
            self.video_dir = VIDEO_OUTPUT_DIR
            self.playlist_file = PLAYLIST_FILE
            self.current_playlist = []
            self.ffmpeg_process = None
            self.is_streaming = False
            
            # Kiểm tra thư mục video
            self._validate_directories()
            
            # Tải playlist hiện có nếu có
            self.load_existing_playlist()
            
            print(f"✅ Khởi tạo LiveStreamManager thành công!")
            print(f"   📁 Thư mục video: {self.video_dir}")
            print(f"   📋 File playlist: {self.playlist_file}")
            print(f"   📊 Số video trong playlist: {len(self.current_playlist)}")
            
        except ImportError as e:
            print(f"❌ Lỗi import config: {e}")
            raise
        except Exception as e:
            print(f"❌ Lỗi khởi tạo LiveStreamManager: {e}")
            raise
    
    def _validate_directories(self):
        """Kiểm tra và tạo thư mục cần thiết"""
        # Kiểm tra thư mục video
        if not os.path.exists(self.video_dir):
            print(f"📁 Tạo thư mục video: {self.video_dir}")
            os.makedirs(self.video_dir, exist_ok=True)
        
        # Kiểm tra file playlist
        playlist_dir = os.path.dirname(self.playlist_file)
        if playlist_dir and not os.path.exists(playlist_dir):
            os.makedirs(playlist_dir, exist_ok=True)
    
    def load_existing_playlist(self):
        """Tải playlist từ file nếu tồn tại"""
        if os.path.exists(self.playlist_file):
            try:
                with open(self.playlist_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # Parse các dòng file trong playlist
                video_paths = []
                for line in lines:
                    line = line.strip()
                    if line.startswith("file '") and line.endswith("'"):
                        video_path = line[6:-1]  # Bỏ "file '" và "'"
                        if os.path.exists(video_path):
                            video_paths.append(video_path)
                
                self.current_playlist = video_paths
                print(f"📋 Đã tải playlist: {len(video_paths)} video")
                
            except Exception as e:
                print(f"⚠️  Không thể đọc playlist: {e}")
                self.current_playlist = []
        else:
            print("📋 Chưa có playlist, sẽ tạo mới")
            self.current_playlist = []
    
    def scan_video_directory(self):
        """Quét thư mục video để tìm file MP4"""
        print(f"\n🔍 Đang quét thư mục video: {self.video_dir}")
        
        if not os.path.exists(self.video_dir):
            print("❌ Thư mục video không tồn tại")
            return []
        
        # Tìm tất cả file .mp4
        video_files = []
        for filename in os.listdir(self.video_dir):
            if filename.lower().endswith('.mp4'):
                full_path = os.path.join(self.video_dir, filename)
                video_files.append(full_path)
        
        # Sắp xếp theo thời gian sửa đổi (mới nhất trước)
        video_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        
        print(f"✅ Tìm thấy {len(video_files)} file MP4")
        
        # Hiển thị danh sách
        for i, video in enumerate(video_files[:10], 1):  # Hiển thị 10 video đầu
            filename = os.path.basename(video)
            size_mb = os.path.getsize(video) / (1024 * 1024)
            mod_time = datetime.fromtimestamp(os.path.getmtime(video))
            print(f"   {i:2d}. {filename[:40]:40s} {size_mb:6.1f} MB  {mod_time:%H:%M %d/%m}")
        
        if len(video_files) > 10:
            print(f"   ... và {len(video_files) - 10} video khác")
        
        return video_files
    
    def create_playlist(self, video_paths=None, playlist_name=None):
        """
        Tạo playlist từ danh sách video
        
        Args:
            video_paths (list): Danh sách đường dẫn video
            playlist_name (str): Tên file playlist (mặc định dùng từ config)
        
        Returns:
            bool: True nếu thành công, False nếu thất bại
        """
        # Xác định file playlist
        if playlist_name:
            playlist_file = playlist_name
        else:
            playlist_file = self.playlist_file
        
        # Nếu không có video_paths, dùng tất cả video trong thư mục
        if video_paths is None:
            video_paths = self.scan_video_directory()
        
        if not video_paths:
            print("❌ Không có video nào để tạo playlist")
            return False
        
        print(f"\n📝 Đang tạo playlist...")
        print(f"   File: {playlist_file}")
        print(f"   Số video: {len(video_paths)}")
        
        try:
            # Tạo nội dung playlist cho FFmpeg
            playlist_content = ""
            for video_path in video_paths:
                if os.path.exists(video_path):
                    # Chuyển đổi đường dẫn sang định dạng phù hợp với FFmpeg
                    abs_path = os.path.abspath(video_path)
                    # Thay thế backslash bằng forward slash cho FFmpeg
                    ffmpeg_path = abs_path.replace('\\', '/')
                    playlist_content += f"file '{ffmpeg_path}'\n"
            
            # Ghi playlist file
            with open(playlist_file, 'w', encoding='utf-8') as f:
                f.write(playlist_content)
            
            # Cập nhật playlist hiện tại
            self.current_playlist = video_paths
            
            print(f"✅ Đã tạo playlist thành công!")
            print(f"   📁 File: {playlist_file}")
            print(f"   📊 {len(video_paths)} video")
            
            # Hiển thị thông tin file
            file_size = os.path.getsize(playlist_file) / 1024  # KB
            print(f"   💾 Kích thước file: {file_size:.1f} KB")
            
            return True
            
        except Exception as e:
            print(f"❌ Lỗi tạo playlist: {e}")
            return False
    
    def add_video_to_playlist(self, video_path, playlist_name=None):
        """
        Thêm một video vào playlist
        
        Args:
            video_path (str): Đường dẫn đến video
            playlist_name (str): Tên file playlist
        
        Returns:
            bool: True nếu thành công
        """
        if not os.path.exists(video_path):
            print(f"❌ Video không tồn tại: {video_path}")
            return False
        
        # Xác định file playlist
        if playlist_name:
            playlist_file = playlist_name
        else:
            playlist_file = self.playlist_file
        
        try:
            # Thêm video vào playlist hiện tại
            self.current_playlist.append(video_path)
            
            # Ghi lại toàn bộ playlist
            return self.create_playlist(self.current_playlist, playlist_file)
            
        except Exception as e:
            print(f"❌ Lỗi thêm video vào playlist: {e}")
            return False
    
    def start_ffmpeg_stream(self, virtual_camera="OBS Virtual Camera", loop_infinite=True):
        """
        Bắt đầu stream playlist với FFmpeg
        
        Args:
            virtual_camera (str): Tên virtual camera output
            loop_infinite (bool): Có lặp vô hạn không
        
        Returns:
            bool: True nếu bắt đầu thành công
        """
        print(f"\n🚀 BẮT ĐẦU FFMPEG STREAM")
        print(f"="*50)
        
        # Kiểm tra playlist
        if not os.path.exists(self.playlist_file):
            print("❌ File playlist không tồn tại")
            print("   Vui lòng tạo playlist trước khi stream")
            return False
        
        # Kiểm tra playlist có nội dung không
        if len(self.current_playlist) == 0:
            print("❌ Playlist trống")
            print("   Thêm video vào playlist trước khi stream")
            return False
        
        print(f"📋 Playlist: {self.playlist_file}")
        print(f"📊 Số video: {len(self.current_playlist)}")
        print(f"🎥 Virtual Camera: {virtual_camera}")
        print(f"🔄 Loop vô hạn: {'Có' if loop_infinite else 'Không'}")
        
        try:
            # Xây dựng command FFmpeg
            ffmpeg_cmd = [
                'ffmpeg',
                '-re',  # Đọc với tốc độ thực
                '-f', 'concat',
                '-safe', '0',
                '-i', self.playlist_file
            ]
            
            # Thêm loop nếu cần
            if loop_infinite:
                ffmpeg_cmd.extend(['-stream_loop', '-1'])
            
            # Thêm output parameters
            # Lưu ý: Virtual camera output phụ thuộc vào hệ điều hành
            if sys.platform == 'win32':
                # Windows - sử dụng dshow
                ffmpeg_cmd.extend([
                    '-f', 'dshow',
                    '-video_size', '1280x720',
                    '-framerate', '30',
                    '-i', f'video={virtual_camera}'
                ])
            elif sys.platform == 'darwin':
                # macOS - sử dụng avfoundation
                ffmpeg_cmd.extend([
                    '-f', 'avfoundation',
                    '-pixel_format', 'uyvy422',
                    '-framerate', '30',
                    '-video_size', '1280x720',
                    '-i', f'"{virtual_camera}"'
                ])
            else:
                # Linux - sử dụng v4l2
                ffmpeg_cmd.extend([
                    '-f', 'v4l2',
                    '-video_size', '1280x720',
                    '-framerate', '30',
                    '-i', '/dev/video2'  # Mặc định cho Linux
                ])
            
            # Hiển thị command để debug
            print(f"\n🔧 FFmpeg command:")
            print(f"   {' '.join(ffmpeg_cmd[:10])}...")
            
            print(f"\n📡 Đang khởi động FFmpeg stream...")
            print(f"   ⚠️  Lưu ý: Giữ terminal này mở để stream tiếp tục")
            print(f"   Nhấn Ctrl+C để dừng stream")
            
            # Chạy FFmpeg
            self.ffmpeg_process = subprocess.Popen(
                ffmpeg_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            self.is_streaming = True
            start_time = time.time()
            
            print(f"\n✅ FFmpeg stream đã bắt đầu!")
            print(f"   🕐 Bắt đầu lúc: {datetime.now().strftime('%H:%M:%S')}")
            print(f"   📊 Playlist: {len(self.current_playlist)} video")
            
            # Đọc output từ FFmpeg để hiển thị tiến trình
            try:
                while self.is_streaming and self.ffmpeg_process.poll() is None:
                    # Đọc stderr để hiển thị thông tin
                    line = self.ffmpeg_process.stderr.readline()
                    if line:
                        # Lọc và hiển thị thông tin hữu ích
                        if 'frame=' in line or 'fps=' in line:
                            print(f"   📹 {line.strip()}")
                    
                    # Kiểm tra mỗi giây
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                print(f"\n⏹️  Nhận tín hiệu dừng...")
                self.stop_ffmpeg_stream()
                return True
            
            return True
            
        except FileNotFoundError:
            print("❌ FFmpeg không được cài đặt hoặc không tìm thấy trong PATH")
            print("   Tải FFmpeg từ: https://ffmpeg.org/download.html")
            return False
        except Exception as e:
            print(f"❌ Lỗi khởi động FFmpeg: {e}")
            return False
    
    def stop_ffmpeg_stream(self):
        """Dừng FFmpeg stream"""
        print(f"\n⏹️  ĐANG DỪNG FFMPEG STREAM...")
        
        if self.ffmpeg_process and self.ffmpeg_process.poll() is None:
            try:
                # Gửi tín hiệu dừng
                self.ffmpeg_process.terminate()
                
                # Chờ process kết thúc
                wait_time = 5
                for i in range(wait_time):
                    if self.ffmpeg_process.poll() is not None:
                        break
                    print(f"   Đang chờ... {i+1}/{wait_time}s")
                    time.sleep(1)
                
                # Nếu vẫn chưa dừng, force kill
                if self.ffmpeg_process.poll() is None:
                    print("   ⚠️  Force kill FFmpeg process...")
                    self.ffmpeg_process.kill()
                    self.ffmpeg_process.wait()
                
                self.is_streaming = False
                print(f"✅ Đã dừng FFmpeg stream")
                
            except Exception as e:
                print(f"❌ Lỗi khi dừng FFmpeg: {e}")
                return False
        
        else:
            print("ℹ️  Không có FFmpeg stream đang chạy")
        
        return True
    
    def create_looping_playlist_for_live(self, duration_hours=8):
        """
        Tạo playlist lặp cho livestream dài
        
        Args:
            duration_hours (int): Số giờ muốn live
        
        Returns:
            bool: True nếu thành công
        """
        print(f"\n🌙 TẠO PLAYLIST CHO LIVE XUYÊN ĐÊM")
        print(f"="*50)
        
        # Quét video hiện có
        available_videos = self.scan_video_directory()
        
        if not available_videos:
            print("❌ Không có video nào trong thư mục")
            return False
        
        print(f"🎬 Video có sẵn: {len(available_videos)}")
        
        # Ước tính tổng thời lượng video
        total_duration = 0
        for video in available_videos:
            # Ước tính thời lượng (giả sử mỗi video khoảng 30-60 giây)
            total_duration += 45  # Giả định trung bình 45 giây
        
        total_hours = total_duration / 3600
        print(f"⏱️  Ước tính thời lượng: {total_hours:.1f} giờ")
        
        # Tính số lần lặp cần thiết
        if total_duration == 0:
            print("❌ Không thể ước tính thời lượng video")
            return False
        
        loops_needed = int((duration_hours * 3600) / total_duration) + 1
        print(f"🔄 Số lần lặp cần thiết: {loops_needed} lần")
        
        # Tạo playlist lặp
        looped_playlist = []
        for _ in range(loops_needed):
            looped_playlist.extend(available_videos)
        
        # Tạo playlist file
        playlist_name = f"live_overnight_{duration_hours}h.txt"
        success = self.create_playlist(looped_playlist, playlist_name)
        
        if success:
            print(f"\n✅ Đã tạo playlist cho live {duration_hours} giờ")
            print(f"   📋 File: {playlist_name}")
            print(f"   🎬 Tổng video (lặp): {len(looped_playlist)}")
            print(f"   ⏱️  Ước tính thời lượng: {duration_hours} giờ")
            print(f"\n⚠️  Lưu ý quan trọng:")
            print(f"   1. Đảm bảo nội dung video đa dạng, tránh lặp quá nhàm chán")
            print(f"   2. Kiểm tra chất lượng video trước khi live")
            print(f"   3. Tuân thủ quy định của TikTok về nội dung")
            
            return True
        else:
            print("❌ Không thể tạo playlist")
            return False
    
    def get_playlist_info(self):
        """Lấy thông tin về playlist hiện tại"""
        if not os.path.exists(self.playlist_file):
            return {
                "exists": False,
                "video_count": 0,
                "file_size": 0,
                "videos": []
            }
        
        try:
            file_size = os.path.getsize(self.playlist_file)
            
            return {
                "exists": True,
                "video_count": len(self.current_playlist),
                "file_size": file_size,
                "file_path": self.playlist_file,
                "videos": self.current_playlist[:10]  # Chỉ lấy 10 video đầu
            }
        except:
            return {
                "exists": False,
                "video_count": 0,
                "file_size": 0,
                "videos": []
            }
    
    def cleanup_old_videos(self, keep_last_n=50):
        """
        Dọn dẹp video cũ, giữ lại n video gần nhất
        
        Args:
            keep_last_n (int): Số video gần nhất cần giữ
        
        Returns:
            tuple: (số video đã xóa, danh sách video còn lại)
        """
        print(f"\n🧹 DỌN DẸP THƯ MỤC VIDEO")
        print(f"="*50)
        
        if not os.path.exists(self.video_dir):
            print("❌ Thư mục video không tồn tại")
            return 0, []
        
        # Lấy tất cả file video
        all_videos = []
        for filename in os.listdir(self.video_dir):
            if filename.lower().endswith('.mp4'):
                full_path = os.path.join(self.video_dir, filename)
                mod_time = os.path.getmtime(full_path)
                all_videos.append((full_path, mod_time, filename))
        
        # Sắp xếp theo thời gian sửa đổi (cũ nhất trước)
        all_videos.sort(key=lambda x: x[1])
        
        total_count = len(all_videos)
        print(f"📊 Tổng số video: {total_count}")
        print(f"💾 Giữ lại: {min(keep_last_n, total_count)} video gần nhất")
        
        # Xác định video cần xóa
        if total_count <= keep_last_n:
            print("✅ Không có video nào cần xóa")
            return 0, [v[0] for v in all_videos]
        
        videos_to_delete = all_videos[:total_count - keep_last_n]
        videos_to_keep = all_videos[total_count - keep_last_n:]
        
        # Xóa video cũ
        deleted_count = 0
        for video_path, mod_time, filename in videos_to_delete:
            try:
                os.remove(video_path)
                deleted_count += 1
                print(f"   🗑️  Đã xóa: {filename}")
            except Exception as e:
                print(f"   ❌ Lỗi xóa {filename}: {e}")
        
        print(f"\n✅ Đã xóa {deleted_count}/{len(videos_to_delete)} video cũ")
        print(f"📊 Còn lại: {len(videos_to_keep)} video")
        
        return deleted_count, [v[0] for v in videos_to_keep]


def test_playlist_functionality():
    """Test các chức năng của LiveStreamManager"""
    print("\n" + "="*60)
    print("🧪 TEST LIVESTREAM MANAGER")
    print("="*60)
    
    try:
        # Khởi tạo manager
        manager = LiveStreamManager()
        
        # Test 1: Quét thư mục video
        print("\n1. 📂 Quét thư mục video...")
        videos = manager.scan_video_directory()
        
        if videos:
            print(f"   ✅ Tìm thấy {len(videos)} video")
            
            # Test 2: Tạo playlist
            print("\n2. 📝 Tạo playlist...")
            if manager.create_playlist(videos[:5]):  # Dùng 5 video đầu
                print("   ✅ Tạo playlist thành công")
                
                # Test 3: Lấy thông tin playlist
                print("\n3. 📊 Lấy thông tin playlist...")
                playlist_info = manager.get_playlist_info()
                print(f"   📋 Tồn tại: {'Có' if playlist_info['exists'] else 'Không'}")
                print(f"   🎬 Số video: {playlist_info['video_count']}")
                print(f"   💾 Kích thước file: {playlist_info['file_size']} bytes")
                
                # Test 4: Tạo playlist cho live xuyên đêm (test ngắn)
                print("\n4. 🌙 Tạo playlist live ngắn (test)...")
                if manager.create_looping_playlist_for_live(duration_hours=0.1):  # 6 phút
                    print("   ✅ Tạo playlist live thành công")
                else:
                    print("   ⚠️  Không thể tạo playlist live")
                
                return True
            else:
                print("   ❌ Không thể tạo playlist")
                return False
        else:
            print("   ℹ️  Không có video để test")
            print("   Tạo video trước khi test playlist")
            return False
            
    except Exception as e:
        print(f"❌ Lỗi test LiveStreamManager: {e}")
        return False


if __name__ == "__main__":
    # Chạy test khi file được thực thi trực tiếp
    test_playlist_functionality()