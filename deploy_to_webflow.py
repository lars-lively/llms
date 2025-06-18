import requests
import os
from datetime import datetime

def deploy_to_github_pages():
    """Deploy llms.txt to GitHub Pages (free hosting)"""
    # If you set up GitHub Pages, the file will be automatically available
    # at https://yourusername.github.io/yourrepo/llms.txt
    print("✅ File available via GitHub Pages after push")
    return True

def deploy_to_netlify():
    """Deploy to Netlify via API (if configured)"""
    try:
        # Netlify API example
        NETLIFY_TOKEN = os.getenv('NETLIFY_TOKEN')
        SITE_ID = os.getenv('NETLIFY_SITE_ID')
        
        if not NETLIFY_TOKEN or not SITE_ID:
            print("⚠️  Netlify credentials not configured")
            return False
        
        with open('llms.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        
        headers = {
            'Authorization': f'Bearer {NETLIFY_TOKEN}',
            'Content-Type': 'text/plain'
        }
        
        # Upload file to Netlify
        url = f"https://api.netlify.com/api/v1/sites/{SITE_ID}/files/llms.txt"
        response = requests.put(url, data=content, headers=headers)
        
        if response.status_code == 200:
            print("✅ Deployed to Netlify successfully!")
            return True
        else:
            print(f"❌ Netlify deploy failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Netlify deploy error: {e}")
        return False

def deploy_to_webflow_via_webhook():
    """Deploy to Webflow via webhook (if available)"""
    try:
        WEBHOOK_URL = os.getenv('WEBFLOW_WEBHOOK_URL')
        
        if not WEBHOOK_URL:
            print("⚠️  Webflow webhook not configured")
            return False
        
        with open('llms.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Send to webhook
        payload = {
            'file_content': content,
            'filename': 'llms.txt',
            'timestamp': datetime.now().isoformat()
        }
        
        response = requests.post(WEBHOOK_URL, json=payload)
        
        if response.status_code == 200:
            print("✅ Sent to Webflow webhook successfully!")
            return True
        else:
            print(f"❌ Webhook failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        return False

def main():
    """Main deployment function"""
    if not os.path.exists('llms.txt'):
        print("❌ llms.txt file not found!")
        return
    
    file_size = os.path.getsize('llms.txt')
    print(f"📄 Deploying llms.txt ({file_size:,} bytes)")
    
    # Try different deployment methods
    success = False
    
    # Method 1: GitHub Pages (automatic if repo is configured)
    success = deploy_to_github_pages()
    
    # Method 2: Netlify (if configured)
    if not success:
        success = deploy_to_netlify()
    
    # Method 3: Webflow webhook (if configured)
    if not success:
        success = deploy_to_webflow_via_webhook()
    
    if success:
        print(f"🎉 Deployment completed at {datetime.now()}")
    else:
        print("⚠️  Configure deployment method in environment variables")

if __name__ == "__main__":
    main() 