#!/usr/bin/env python3
"""Search for volcengine AI audio-video interaction solution"""

from coze_coding_dev_sdk import SearchClient
from coze_coding_utils.runtime_ctx.context import new_context

def search_volcengine_info():
    """Search for volcengine AI audio-video solution"""
    ctx = new_context(method="search.web")
    client = SearchClient(ctx=ctx)
    
    # Search for volcengine AI audio-video solution
    queries = [
        "火山引擎 AI 音视频互动 方案 机器人",
        "Volcengine AI Agent 机器人控制系统 Linux",
        "火山引擎 RTC 硬件对话智能体 Linux SDK",
        "火山引擎 AI 音视频 工具调用 知识库",
        "火山引擎 机器人 Demo C++ Linux"
    ]
    
    all_results = []
    
    for query in queries:
        print(f"\n{'='*60}")
        print(f"Searching: {query}")
        print('='*60)
        
        response = client.web_search(
            query=query,
            count=10,
            need_summary=True
        )
        
        if response.web_items:
            for item in response.web_items:
                print(f"\nTitle: {item.title}")
                print(f"URL: {item.url}")
                print(f"Summary: {item.summary}")
                print("-"*60)
                all_results.append({
                    'title': item.title,
                    'url': item.url,
                    'summary': item.summary,
                    'query': query
                })
        else:
            print("No results found")
    
    # Save results
    with open('/workspace/projects/volc_engine_search_results.md', 'w', encoding='utf-8') as f:
        f.write("# 火山引擎AI音视频互动方案搜索结果\n\n")
        for i, result in enumerate(all_results, 1):
            f.write(f"## {i}. {result['title']}\n")
            f.write(f"- URL: {result['url']}\n")
            f.write(f"- Query: {result['query']}\n")
            f.write(f"- Summary: {result['summary']}\n\n")
    
    print(f"\n{'='*60}")
    print(f"Total results: {len(all_results)}")
    print(f"Results saved to /workspace/projects/volc_engine_search_results.md")
    print('='*60)

if __name__ == "__main__":
    search_volcengine_info()
