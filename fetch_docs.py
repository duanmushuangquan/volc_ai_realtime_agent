#!/usr/bin/env python3
"""Fetch volcengine documentation for AI audio-video interaction solution"""

from coze_coding_dev_sdk.fetch import FetchClient
from coze_coding_utils.runtime_ctx.context import Context

def fetch_doc(url, filename):
    """Fetch documentation from URL and save to file"""
    # 不使用Context，直接创建客户端
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
    # Fetch both documentation pages
    docs = [
        ("https://www.volcengine.com/docs/6348/?lang=zh", "/workspace/projects/volc_engine_overview.md"),
        ("https://www.volcengine.com/docs/6348/131050?lang=zh", "/workspace/projects/volc_engine_linux_demo.md")
    ]
    
    for url, filename in docs:
        print(f"\n{'='*50}")
        print(f"Fetching: {url}")
        print(f"{'='*50}")
        success = fetch_doc(url, filename)
        if success:
            print(f"✓ Successfully fetched {url}")
        else:
            print(f"✗ Failed to fetch {url}")
