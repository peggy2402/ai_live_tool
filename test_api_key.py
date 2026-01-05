# test_api_key.py
import base64
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv('D_ID_API_KEY')
print(f"API Key hiện tại: {key}")
print(f"Độ dài: {len(key)} ký tự")

# Kiểm tra nếu là base64 encoded
if key and ':' in key:
    username, password = key.split(':', 1)
    print(f"\nPhát hiện format username:password")
    print(f"Username (sau khi decode base64):")
    try:
        decoded_user = base64.b64decode(username).decode('utf-8')
        print(f"  {decoded_user}")
    except:
        print(f"  Không thể decode: {username}")
    
    print(f"Password: {password[:10]}...")
    
print(f"\nĐịnh dạng D-ID API Key thật nên bắt đầu bằng 'sk_'")
print(f"Key của bạn bắt đầu bằng 'sk_'? {key.startswith('sk_')}")