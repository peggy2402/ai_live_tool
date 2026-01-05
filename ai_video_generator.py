"""
ai_video_generator.py - Tạo video AI avatar từ D-ID API
Xử lý đầy đủ: tạo video, theo dõi tiến trình, tải về, và xử lý lỗi
"""

import requests
import time
import os
import json
import sys
from datetime import datetime

class AIVideoGenerator:
    """
    Lớp tạo video AI avatar sử dụng D-ID API
    Hỗ trợ cả Basic Auth (username:password) và Bearer Token (sk_...)
    """
    
    def __init__(self):
        """Khởi tạo generator với cấu hình từ config"""
        try:
            from config import (
                D_ID_API_KEY, D_ID_AUTH_HEADER, D_ID_API_URL,
                TTS_VOICE_ID, VIDEO_OUTPUT_DIR, MAX_RETRIES, REQUEST_TIMEOUT
            )
            
            self.api_key = D_ID_API_KEY
            self.auth_header = D_ID_AUTH_HEADER
            self.api_url = D_ID_API_URL
            self.voice_id = TTS_VOICE_ID
            self.video_dir = VIDEO_OUTPUT_DIR
            self.max_retries = MAX_RETRIES
            self.timeout = REQUEST_TIMEOUT
            
            # Kiểm tra cấu hình cơ bản
            self._validate_config()
            
            # Thiết lập headers cho API request
            self.headers = {
                "Authorization": self.auth_header,
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            # Biến theo dõi trạng thái
            self.total_videos_created = 0
            self.last_video_path = None
            
            print(f"✅ Khởi tạo AIVideoGenerator thành công!")
            print(f"   • Giọng nói: {self.voice_id}")
            print(f"   • Thư mục lưu: {self.video_dir}")
            print(f"   • Số lần thử lại tối đa: {self.max_retries}")
            
        except ImportError as e:
            print(f"❌ Lỗi import config: {e}")
            print("   Đảm bảo file config.py tồn tại trong cùng thư mục")
            raise
        except Exception as e:
            print(f"❌ Lỗi khởi tạo AIVideoGenerator: {e}")
            raise
    
    def _validate_config(self):
        """Kiểm tra cấu hình có hợp lệ không"""
        if not self.api_key:
            raise ValueError("API Key không được để trống")
        
        if not self.auth_header:
            raise ValueError("Authorization header không được để trống")
        
        if not self.api_url:
            raise ValueError("API URL không được để trống")
        
        print(f"🔍 Đang kiểm tra kết nối API...")
        
        # Test kết nối đơn giản
        try:
            test_response = requests.get(
                f"{self.api_url}/talks",
                headers={"Authorization": self.auth_header},
                timeout=10
            )
            
            if test_response.status_code in [200, 401, 403]:
                print(f"   ✅ Kết nối API thành công (status: {test_response.status_code})")
            else:
                print(f"   ⚠️  Kết nối API bất thường (status: {test_response.status_code})")
                
        except requests.exceptions.ConnectionError:
            print("   ❌ Không thể kết nối đến D-ID API")
            print("   Kiểm tra kết nối internet và URL API")
        except Exception as e:
            print(f"   ⚠️  Lỗi kiểm tra kết nối: {e}")
    
    def create_talking_head_video(self, script_text, presenter_image_url, output_filename, retry_count=0):
        """
        Tạo video AI avatar nói từ kịch bản
        
        Args:
            script_text (str): Kịch bản văn bản cần chuyển thành giọng nói
            presenter_image_url (str): URL ảnh khuôn mặt cho avatar
            output_filename (str): Tên file đầu ra (không cần .mp4)
            retry_count (int): Số lần đã thử lại (dùng cho đệ quy)
        
        Returns:
            str: Đường dẫn đến file video đã tạo, hoặc None nếu thất bại
        """
        print(f"\n{'='*60}")
        print(f"🎬 BẮT ĐẦU TẠO VIDEO: {output_filename}")
        print(f"{'='*60}")
        
        # Kiểm tra đầu vào
        if not script_text or len(script_text.strip()) < 10:
            print("❌ Script quá ngắn (cần ít nhất 10 ký tự)")
            return None
        
        if not presenter_image_url or not presenter_image_url.startswith(('http://', 'https://')):
            print("❌ URL ảnh không hợp lệ")
            return None
        
        # Đếm số từ trong script
        word_count = len(script_text.split())
        print(f"📝 Script: {word_count} từ, ~{len(script_text)} ký tự")
        print(f"🖼️  Ảnh avatar: {presenter_image_url[:50]}...")
        
        # 1. Chuẩn bị payload cho API
        payload = {
            "script": {
                "type": "text",
                "provider": {
                    "type": "microsoft",
                    "voice_id": self.voice_id
                },
                "input": script_text,
                "subtitles": False
            },
            "source_url": presenter_image_url,
            "config": {
                "fluent": True,
                "pad_audio": 0.0,
                "result_format": "mp4",
                "stitch": True
            }
        }
        
        # 2. Gửi request tạo video
        try:
            print(f"\n🔄 Đang gửi yêu cầu đến D-ID API...")
            print(f"   URL: {self.api_url}/talks")
            print(f"   Timeout: {self.timeout}s")
            
            start_time = time.time()
            
            response = requests.post(
                f"{self.api_url}/talks",
                headers=self.headers,
                json=payload,
                timeout=self.timeout
            )
            
            request_time = time.time() - start_time
            print(f"   ⏱️  Thời gian phản hồi: {request_time:.2f}s")
            print(f"   📊 Status code: {response.status_code}")
            
            # Xử lý response
            if response.status_code == 201:
                response_data = response.json()
                talk_id = response_data.get('id')
                
                if not talk_id:
                    print("❌ API không trả về ID video")
                    return None
                
                print(f"✅ Đã tạo job video thành công!")
                print(f"   Job ID: {talk_id}")
                print(f"   Est. Duration: {response_data.get('duration', 'N/A')}s")
                print(f"   Created at: {response_data.get('created_at', 'N/A')}")
                
                # 3. Theo dõi tiến trình tạo video
                video_url = self._monitor_video_creation(talk_id)
                
                if video_url:
                    # 4. Tải video về
                    video_path = self._download_video_file(video_url, output_filename)
                    
                    if video_path:
                        self.total_videos_created += 1
                        self.last_video_path = video_path
                        
                        print(f"\n{'='*60}")
                        print(f"🎉 TẠO VIDEO THÀNH CÔNG!")
                        print(f"{'='*60}")
                        print(f"📁 File: {video_path}")
                        
                        # Hiển thị thông tin file
                        try:
                            file_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
                            print(f"📊 Kích thước: {file_size:.2f} MB")
                            print(f"🔄 Tổng số video đã tạo: {self.total_videos_created}")
                        except:
                            pass
                        
                        return video_path
                    else:
                        print("❌ Không thể tải video về")
                        return None
                else:
                    print("❌ Không thể lấy URL video sau khi xử lý")
                    
                    # Thử lại nếu chưa quá số lần cho phép
                    if retry_count < self.max_retries:
                        print(f"🔄 Thử lại lần {retry_count + 1}/{self.max_retries}...")
                        return self.create_talking_head_video(
                            script_text, presenter_image_url, 
                            output_filename, retry_count + 1
                        )
                    else:
                        print("❌ Đã vượt quá số lần thử lại tối đa")
                        return None
                        
            elif response.status_code == 401:
                print("❌ Lỗi xác thực: API Key không hợp lệ hoặc hết hạn")
                print("   Kiểm tra lại API Key trong file .env")
                return None
                
            elif response.status_code == 402:
                print("❌ Hết credit: Tài khoản D-ID không đủ credit")
                print("   Vui lòng nạp thêm credit tại https://studio.d-id.com")
                return None
                
            elif response.status_code == 429:
                print("❌ Quá nhiều request: Vượt quá giới hạn API")
                wait_time = 60  # Chờ 60 giây
                print(f"   ⏳ Chờ {wait_time}s trước khi thử lại...")
                time.sleep(wait_time)
                
                if retry_count < self.max_retries:
                    return self.create_talking_head_video(
                        script_text, presenter_image_url, 
                        output_filename, retry_count + 1
                    )
                return None
                
            else:
                print(f"❌ Lỗi API không xác định: {response.status_code}")
                print(f"   Chi tiết lỗi: {response.text[:200]}")
                
                if retry_count < self.max_retries:
                    print(f"🔄 Thử lại lần {retry_count + 1}/{self.max_retries}...")
                    time.sleep(5)  # Chờ 5 giây trước khi thử lại
                    return self.create_talking_head_video(
                        script_text, presenter_image_url, 
                        output_filename, retry_count + 1
                    )
                return None
                
        except requests.exceptions.Timeout:
            print("❌ Timeout: Request mất quá nhiều thời gian")
            
            if retry_count < self.max_retries:
                print(f"🔄 Thử lại lần {retry_count + 1}/{self.max_retries}...")
                return self.create_talking_head_video(
                    script_text, presenter_image_url, 
                    output_filename, retry_count + 1
                )
            return None
            
        except requests.exceptions.ConnectionError:
            print("❌ Lỗi kết nối: Không thể kết nối đến D-ID API")
            print("   Kiểm tra kết nối internet của bạn")
            return None
            
        except Exception as e:
            print(f"❌ Lỗi không xác định: {type(e).__name__}: {e}")
            
            if retry_count < self.max_retries:
                print(f"🔄 Thử lại lần {retry_count + 1}/{self.max_retries}...")
                time.sleep(3)
                return self.create_talking_head_video(
                    script_text, presenter_image_url, 
                    output_filename, retry_count + 1
                )
            return None
    
    def _monitor_video_creation(self, talk_id, max_attempts=30, delay_seconds=3):
        """
        Theo dõi tiến trình tạo video
        
        Args:
            talk_id (str): ID của job video
            max_attempts (int): Số lần kiểm tra tối đa
            delay_seconds (int): Thời gian chờ giữa các lần kiểm tra
        
        Returns:
            str: URL video khi hoàn thành, hoặc None nếu thất bại
        """
        print(f"\n📊 Đang theo dõi tiến trình video...")
        print(f"   Job ID: {talk_id}")
        print(f"   Số lần kiểm tra tối đa: {max_attempts}")
        print(f"   Thời gian chờ mỗi lần: {delay_seconds}s")
        
        for attempt in range(1, max_attempts + 1):
            try:
                # Hiển thị progress bar đơn giản
                progress = (attempt / max_attempts) * 100
                print(f"\r   [{attempt:02d}/{max_attempts:02d}] Đang xử lý... {progress:.1f}%", end="")
                
                # Kiểm tra trạng thái
                status_response = requests.get(
                    f"{self.api_url}/talks/{talk_id}",
                    headers=self.headers,
                    timeout=10
                )
                
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    status = status_data.get('status')
                    
                    if status == 'done':
                        print(f"\n✅ Video đã hoàn thành!")
                        
                        result_url = status_data.get('result_url')
                        duration = status_data.get('duration', 'N/A')
                        
                        print(f"   📍 Video URL: {result_url[:80]}..." if len(result_url) > 80 else f"   📍 Video URL: {result_url}")
                        print(f"   ⏱️  Thời lượng: {duration}s")
                        print(f"   ✅ Hoàn thành sau {attempt} lần kiểm tra")
                        
                        return result_url
                        
                    elif status == 'error':
                        error_msg = status_data.get('error', 'Lỗi không xác định')
                        print(f"\n❌ Lỗi tạo video: {error_msg}")
                        return None
                        
                    elif status in ['pending', 'started', 'processing']:
                        # Tiếp tục chờ
                        time.sleep(delay_seconds)
                        continue
                        
                    else:
                        print(f"\n⚠️  Trạng thái không xác định: {status}")
                        time.sleep(delay_seconds)
                        continue
                        
                elif status_response.status_code == 404:
                    print(f"\n❌ Không tìm thấy job ID: {talk_id}")
                    return None
                    
                else:
                    print(f"\n⚠️  Lỗi kiểm tra trạng thái: {status_response.status_code}")
                    time.sleep(delay_seconds)
                    continue
                    
            except requests.exceptions.RequestException as e:
                print(f"\n⚠️  Lỗi kết nối khi kiểm tra: {e}")
                
                if attempt < max_attempts:
                    time.sleep(delay_seconds * 2)  # Chờ lâu hơn nếu có lỗi kết nối
                else:
                    print("❌ Đã vượt quá số lần thử tối đa")
                    return None
        
        print(f"\n❌ Quá thời gian chờ tạo video ({max_attempts * delay_seconds}s)")
        return None
    
    def _download_video_file(self, video_url, output_filename):
        """
        Tải video từ URL về máy
        
        Args:
            video_url (str): URL của video
            output_filename (str): Tên file đầu ra
        
        Returns:
            str: Đường dẫn đến file đã tải, hoặc None nếu thất bại
        """
        print(f"\n📥 Đang tải video về máy...")
        print(f"   Source: {video_url[:80]}..." if len(video_url) > 80 else f"   Source: {video_url}")
        
        try:
            # Tạo tên file với timestamp để tránh trùng lặp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_filename = f"{output_filename}_{timestamp}"
            file_path = os.path.join(self.video_dir, f"{safe_filename}.mp4")
            
            # Tải video với stream để xử lý file lớn
            start_time = time.time()
            
            with requests.get(video_url, stream=True, timeout=60) as response:
                response.raise_for_status()
                
                total_size = int(response.headers.get('content-length', 0))
                downloaded_size = 0
                
                print(f"   📁 Lưu tại: {file_path}")
                
                if total_size > 0:
                    print(f"   📊 Kích thước: {total_size / (1024*1024):.2f} MB")
                
                # Tải và lưu file
                with open(file_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)
                            downloaded_size += len(chunk)
                            
                            # Hiển thị tiến trình nếu biết tổng size
                            if total_size > 0:
                                percent = (downloaded_size / total_size) * 100
                                print(f"\r   📥 Đang tải... {percent:.1f}%", end="")
                
                download_time = time.time() - start_time
                print(f"\n✅ Tải xuống hoàn tất!")
                print(f"   ⏱️  Thời gian tải: {download_time:.2f}s")
                
                # Kiểm tra file đã tải
                if os.path.exists(file_path):
                    actual_size = os.path.getsize(file_path)
                    print(f"   ✅ File đã lưu: {actual_size / 1024:.1f} KB")
                    return file_path
                else:
                    print("❌ File không tồn tại sau khi tải")
                    return None
                    
        except requests.exceptions.RequestException as e:
            print(f"❌ Lỗi tải video: {e}")
            return None
        except IOError as e:
            print(f"❌ Lỗi ghi file: {e}")
            return None
        except Exception as e:
            print(f"❌ Lỗi không xác định khi tải video: {e}")
            return None
    
    def get_stats(self):
        """Lấy thống kê về video đã tạo"""
        return {
            "total_videos": self.total_videos_created,
            "last_video": self.last_video_path,
            "voice_id": self.voice_id,
            "output_dir": self.video_dir
        }
    
    def test_connection(self):
        """Test kết nối đến D-ID API"""
        print("\n🔍 Kiểm tra kết nối D-ID API...")
        
        try:
            response = requests.get(
                f"{self.api_url}/talks",
                headers=self.headers,
                timeout=10
            )
            
            print(f"   Status code: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Kết nối API thành công!")
                return True
            elif response.status_code == 401:
                print("❌ Lỗi xác thực: API Key không hợp lệ")
                return False
            else:
                print(f"⚠️  Phản hồi không mong đợi: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Lỗi kết nối: {e}")
            return False


def test_single_video_creation():
    """Hàm test tạo một video mẫu"""
    print("\n" + "="*60)
    print("🧪 TEST TẠO VIDEO MẪU")
    print("="*60)
    
    try:
        # Khởi tạo generator
        generator = AIVideoGenerator()
        
        # Test kết nối trước
        if not generator.test_connection():
            print("❌ Không thể kết nối đến API, dừng test")
            return None
        
        # Thông tin video test
        test_script = """
        Xin chào các bạn! Tôi là AI Avatar được tạo bởi D-ID.
        Đây là video thử nghiệm cho công cụ AI Livestream.
        Chúng ta sẽ cùng nhau khám phá những sản phẩm thời trang mới.
        Hãy theo dõi và ủng hộ chúng tôi nhé!
        """
        
        # URL ảnh mẫu từ D-ID (free to use)
        test_image_url = "https://cdn.ohanapreschool.edu.vn/wp-content/uploads/2025/12/anh-gai-xinh-vu-to-viet-nam-1.jpg"
        
        print(f"\n📝 Script test: {len(test_script)} ký tự")
        print(f"🖼️  Ảnh mẫu: {test_image_url}")
        
        # Tạo video
        result = generator.create_talking_head_video(
            script_text=test_script,
            presenter_image_url=test_image_url,
            output_filename="test_demo"
        )
        
        if result:
            print("\n🎉 TEST THÀNH CÔNG!")
            print(f"Video đã được lưu tại: {result}")
        else:
            print("\n❌ TEST THẤT BẠI")
            print("Vui lòng kiểm tra:")
            print("1. API Key trong file .env")
            print("2. Kết nối internet")
            print("3. Credit tài khoản D-ID")
        
        return result
        
    except Exception as e:
        print(f"❌ Lỗi trong quá trình test: {e}")
        return None


if __name__ == "__main__":
    # Chạy test khi file được thực thi trực tiếp
    test_single_video_creation()