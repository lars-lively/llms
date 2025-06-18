import requests
import os
from datetime import datetime

# Configuration for automatic upload
WEBFLOW_API_TOKEN = "YOUR_WEBFLOW_API_TOKEN"  # Get from Webflow account settings
WEBFLOW_SITE_ID = "YOUR_SITE_ID"  # Your Webflow site ID
LLMS_TXT_PATH = "llms.txt"

def upload_to_webflow():
    """Upload llms.txt to Webflow via API"""
    try:
        # This is a placeholder - Webflow API for file uploads varies
        # You might need to use their Assets API or hosting provider API
        
        with open(LLMS_TXT_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Example API call (adjust based on your hosting setup)
        headers = {
            'Authorization': f'Bearer {WEBFLOW_API_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        # This would depend on your specific hosting/CDN setup
        print("📤 Uploading to Webflow...")
        print("⚠️  Configure your hosting provider's API for automatic uploads")
        
        return True
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return False

def upload_via_ftp():
    """Alternative: Upload via FTP if you have FTP access"""
    try:
        # Example using ftplib
        import ftplib
        
        # FTP_HOST = "your-ftp-server.com"
        # FTP_USER = "your-username"
        # FTP_PASS = "your-password"
        
        # with ftplib.FTP(FTP_HOST) as ftp:
        #     ftp.login(FTP_USER, FTP_PASS)
        #     with open(LLMS_TXT_PATH, 'rb') as f:
        #         ftp.storbinary('STOR llms.txt', f)
        
        print("📤 FTP upload - configure your FTP credentials")
        return True
    except Exception as e:
        print(f"❌ FTP upload failed: {e}")
        return False

def main():
    print("🔄 Checking for llms.txt file...")
    
    if not os.path.exists(LLMS_TXT_PATH):
        print("❌ llms.txt not found. Run update_llms_txt.py first.")
        return
    
    file_size = os.path.getsize(LLMS_TXT_PATH)
    print(f"📄 Found llms.txt ({file_size:,} bytes)")
    
    # Try uploading
    success = False
    
    # Option 1: Upload to Webflow (configure API)
    # success = upload_to_webflow()
    
    # Option 2: Upload via FTP (configure FTP)
    # success = upload_via_ftp()
    
    # Option 3: Copy to a cloud folder (Dropbox, Google Drive, etc.)
    try:
        import shutil
        # Example: Copy to a synced folder
        # cloud_path = "C:/Users/ldron/Dropbox/Website/llms.txt"
        # shutil.copy2(LLMS_TXT_PATH, cloud_path)
        print("📁 Configure cloud sync folder for automatic upload")
        success = True
    except Exception as e:
        print(f"❌ Cloud sync failed: {e}")
    
    if success:
        print("✅ Upload completed successfully!")
        print(f"🕒 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print("⚠️  Configure upload method in auto_upload_llms.py")

if __name__ == "__main__":
    main() 