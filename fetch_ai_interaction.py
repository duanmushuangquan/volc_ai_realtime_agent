#!/usr/bin/env python3
"""Fetch volcengine AI audio-video interaction solution documentation"""

from coze_coding_dev_sdk.fetch import FetchClient

def fetch_doc(url, filename):
    """Fetch documentation from URL and save to file"""
    client = FetchClient()
    
    print(f"Fetching: {url}")
    response = client.fetch(url=url)
    
    if response.status_code == 0:
        # Extract text content
        text_content = []
        for item in response.content:
            if item.type == "text":
                text_content.append(item.text)
        
        full_content = f"""
Title: {response.title}
URL: {response.url}
Publish Time: {response.publish_time}
File Type: {response.filetype}
========================================

Content:
{chr(10).join(text_content)}
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        print(f"Saved to {filename}")
        print(f"Content length: {len(full_content)} chars")
        return True
    else:
        print(f"Failed to fetch: {response.status_message}")
        return False

if __name__ == "__main__":
    # Main AI audio-video interaction solution document
    docs = [
        ("https://www.volcengine.com/docs/6348/1544162?lang=zh", "/workspace/projects/volc_ai_interaction.md"),
        # Also fetch related docs
        ("https://www.volcengine.com/docs/6348/1544163?lang=zh", "/workspace/projects/volc_ai_interaction_quickstart.md"),
        ("https://www.volcengine.com/docs/6348/1544164?lang=zh", "/workspace/projects/volc_ai_interaction_demo.md"),
    ]
    
    for url, filename in docs:
        print(f"\n{'='*60}")
        print(f"Fetching: {url}")
        print(f"{'='*60}")
        try:
            success = fetch_doc(url, filename)
            if success:
                print(f"✓ Successfully fetched")
        except Exception as e:
            print(f"✗ Error: {e}")
