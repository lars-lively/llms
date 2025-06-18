import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from urllib.parse import urlparse

# CONFIGURATION
SITEMAP_URL = 'https://www.lively.nl/sitemap.xml'
CONTACT_EMAIL = 'info@lively.nl'
DISALLOWED_PATHS = ['/private/', '/user-data/']
ATTRIBUTION_REQUIRED = True
DATA_REMOVAL_EMAIL = 'info@lively.nl'
LLMS_TXT_PATH = 'llms.txt'


def fetch_comprehensive_metadata(url):
    """Fetch comprehensive metadata from a webpage"""
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Basic metadata
        title = soup.title.string.strip() if soup.title else ''
        lang = soup.html.get('lang', 'nl') if soup.html else 'nl'
        
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        description = meta_desc.get('content', '').strip() if meta_desc else ''
        
        # Meta keywords
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        keywords = [k.strip() for k in meta_keywords.get('content', '').split(',')] if meta_keywords and meta_keywords.get('content') else []
        
        # Author
        meta_author = soup.find('meta', attrs={'name': 'author'})
        author = meta_author.get('content', '').strip() if meta_author else ''
        
        # Page type/category (try to determine from URL structure)
        parsed_url = urlparse(url)
        path_parts = [p for p in parsed_url.path.split('/') if p]
        page_type = path_parts[0] if path_parts else 'home'
        
        # Content analysis
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        text_content = soup.get_text()
        lines = (line.strip() for line in text_content.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = ' '.join(chunk for chunk in chunks if chunk)
        
        content_length = len(clean_text)
        word_count = len(clean_text.split())
        
        # Try to extract main headings
        headings = []
        for h_tag in soup.find_all(['h1', 'h2', 'h3']):
            heading_text = h_tag.get_text().strip()
            if heading_text:
                headings.append(heading_text)
        
        # Extract any schema.org structured data
        schema_type = ''
        schema_script = soup.find('script', {'type': 'application/ld+json'})
        if schema_script:
            try:
                import json
                schema_data = json.loads(schema_script.string)
                if isinstance(schema_data, dict) and '@type' in schema_data:
                    schema_type = schema_data['@type']
                elif isinstance(schema_data, list) and len(schema_data) > 0 and '@type' in schema_data[0]:
                    schema_type = schema_data[0]['@type']
            except:
                pass
        
        # Generate tags based on content analysis
        auto_tags = []
        if 'event' in clean_text.lower() or 'evenement' in clean_text.lower():
            auto_tags.append('event')
        if 'software' in clean_text.lower():
            auto_tags.append('software')
        if 'registratie' in clean_text.lower():
            auto_tags.append('registratie')
        if 'app' in clean_text.lower():
            auto_tags.append('app')
        if 'contact' in url.lower() or 'contact' in title.lower():
            auto_tags.append('contact')
        if 'about' in url.lower() or 'over-ons' in url.lower():
            auto_tags.append('about')
        if 'cases' in url.lower() or 'case' in title.lower():
            auto_tags.append('cases')
        if 'blog' in url.lower() or 'insights' in url.lower():
            auto_tags.append('blog')
        if 'pricing' in url.lower() or 'prijs' in url.lower():
            auto_tags.append('pricing')
        
        # Combine all tags
        all_tags = list(set(keywords + auto_tags))
        
        return {
            'title': title,
            'description': description,
            'language': lang,
            'author': author,
            'page_type': page_type,
            'tags': all_tags,
            'content_length': content_length,
            'word_count': word_count,
            'headings': headings[:3],  # First 3 headings
            'schema_type': schema_type
        }
        
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return {
            'title': '',
            'description': '',
            'language': 'nl',
            'author': '',
            'page_type': 'unknown',
            'tags': [],
            'content_length': 0,
            'word_count': 0,
            'headings': [],
            'schema_type': ''
        }


def fetch_sitemap_urls(sitemap_url):
    try:
        resp = requests.get(sitemap_url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'xml')
        urls = []
        for url_tag in soup.find_all('url'):
            loc = url_tag.find('loc').text.strip()
            lastmod = url_tag.find('lastmod').text.strip() if url_tag.find('lastmod') else ''
            
            # Extract priority and changefreq if available
            priority = url_tag.find('priority')
            priority_val = priority.text.strip() if priority else ''
            
            changefreq = url_tag.find('changefreq')
            changefreq_val = changefreq.text.strip() if changefreq else ''
            
            urls.append({
                'url': loc, 
                'lastmod': lastmod,
                'priority': priority_val,
                'changefreq': changefreq_val
            })
        return urls
    except Exception as e:
        print(f"Error fetching sitemap: {e}")
        return []


def generate_detailed_llms_txt(entries):
    now = datetime.now().strftime('%Y-%m-%d')
    header = f"""# llms.txt for lively.nl
# Last updated: {now}
# Generated automatically by Lively website scraper
# Total pages: {len(entries)}

Contact: {CONTACT_EMAIL}

Allow-LLM: yes
Disallow-Paths: {', '.join(DISALLOWED_PATHS)}
Attribution-Required: {'yes' if ATTRIBUTION_REQUIRED else 'no'}

# Data Removal
Data-Removal-Request: {DATA_REMOVAL_EMAIL}

# Website Information
# Domain: lively.nl
# Language: Dutch (nl)
# Industry: Event Technology & Software
# Description: Lively specializes in event technology solutions including registration software, event apps, and comprehensive event management systems.

# Public Pages with Detailed Metadata

"""
    
    body = ''
    for entry in entries:
        body += f"- url: {entry['url']}\n"
        
        if entry['metadata']['title']:
            body += f"  title: {entry['metadata']['title']}\n"
        
        if entry['metadata']['description']:
            # Truncate description if too long
            desc = entry['metadata']['description']
            if len(desc) > 200:
                desc = desc[:197] + "..."
            body += f"  description: {desc}\n"
        
        body += f"  language: {entry['metadata']['language']}\n"
        
        if entry['lastmod']:
            body += f"  lastmod: {entry['lastmod']}\n"
        
        if entry['metadata']['author']:
            body += f"  author: {entry['metadata']['author']}\n"
        
        body += f"  page_type: {entry['metadata']['page_type']}\n"
        
        if entry['metadata']['tags']:
            body += f"  tags: {entry['metadata']['tags']}\n"
        
        body += f"  content_length: {entry['metadata']['content_length']}\n"
        body += f"  word_count: {entry['metadata']['word_count']}\n"
        
        if entry['metadata']['headings']:
            body += f"  main_headings: {entry['metadata']['headings']}\n"
        
        if entry['metadata']['schema_type']:
            body += f"  schema_type: {entry['metadata']['schema_type']}\n"
        
        if entry['priority']:
            body += f"  sitemap_priority: {entry['priority']}\n"
        
        if entry['changefreq']:
            body += f"  update_frequency: {entry['changefreq']}\n"
        
        body += "\n"
    
    # Add statistics
    total_words = sum(entry['metadata']['word_count'] for entry in entries)
    avg_words = total_words // len(entries) if entries else 0
    
    footer = f"""
# Website Statistics
# Total pages analyzed: {len(entries)}
# Total word count: {total_words:,}
# Average words per page: {avg_words:,}
# Languages: {', '.join(set(entry['metadata']['language'] for entry in entries))}
# Page types: {', '.join(set(entry['metadata']['page_type'] for entry in entries))}

# Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    return header + body + footer


def main():
    print("Fetching URLs from sitemap...")
    urls = fetch_sitemap_urls(SITEMAP_URL)
    if not urls:
        print("No URLs found. Please check your sitemap or provide URLs manually.")
        return
    
    print(f"Found {len(urls)} URLs. Fetching detailed metadata...")
    entries = []
    
    for i, entry in enumerate(urls, 1):
        print(f"Processing {i}/{len(urls)}: {entry['url']}")
        metadata = fetch_comprehensive_metadata(entry['url'])
        entries.append({
            'url': entry['url'],
            'lastmod': entry['lastmod'],
            'priority': entry['priority'],
            'changefreq': entry['changefreq'],
            'metadata': metadata
        })
    
    print("Generating detailed llms.txt...")
    llms_txt_content = generate_detailed_llms_txt(entries)
    
    with open(LLMS_TXT_PATH, 'w', encoding='utf-8') as f:
        f.write(llms_txt_content)
    
    print(f"✅ llms.txt updated with {len(entries)} detailed entries!")
    print(f"📊 Total content analyzed: {sum(e['metadata']['word_count'] for e in entries):,} words")


if __name__ == "__main__":
    main() 