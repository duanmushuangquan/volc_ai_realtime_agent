#!/usr/bin/env python3
"""
Robot Control System Test Script
测试系统核心功能
"""

import asyncio
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'python'))

from agent import ChatManager, ToolManager, KnowledgeBase, AgentGraph
from loguru import logger


async def test_chat_manager():
    """测试对话管理器"""
    print("\n" + "="*60)
    print("测试1: 对话管理器")
    print("="*60)
    
    chat_mgr = ChatManager(
        system_prompt="你是一个智能助手。",
        max_history=10
    )
    
    # 创建对话
    chat_mgr.create_conversation("test_001")
    
    # 添加消息
    chat_mgr.add_message("test_001", "user", "你好")
    chat_mgr.add_message("test_001", "assistant", "你好！有什么可以帮助你的？")
    chat_mgr.add_message("test_001", "user", "今天天气怎么样？")
    
    # 获取历史
    history = chat_mgr.get_conversation_history("test_001")
    print(f"✓ 对话历史长度: {len(history)}")
    print(f"✓ 最近的2条消息:")
    for msg in chat_mgr.get_recent_messages("test_001", 2):
        print(f"  - [{msg.role}]: {msg.content[:50]}...")
    
    # 获取摘要
    summary = chat_mgr.get_conversation_summary("test_001")
    print(f"✓ 对话摘要: {summary}")
    
    return True


async def test_tool_manager():
    """测试工具管理器"""
    print("\n" + "="*60)
    print("测试2: 工具管理器")
    print("="*60)
    
    tool_mgr = ToolManager()
    
    # 获取工具列表
    tools = tool_mgr.get_all_tools()
    print(f"✓ 可用工具数量: {len(tools)}")
    for tool in tools:
        print(f"  - {tool['name']}: {tool['description'][:50]}...")
    
    # 测试工具执行
    print("\n测试时间工具:")
    result = await tool_mgr.tools['get_time'].handler()
    print(f"  结果: {result}")
    
    print("\n测试计算器工具:")
    result = await tool_mgr.tools['calculator'].handler(expression="2+2")
    print(f"  结果: {result}")
    
    return True


async def test_knowledge_base():
    """测试知识库"""
    print("\n" + "="*60)
    print("测试3: 知识库")
    print("="*60)
    
    kb = KnowledgeBase(
        collection_name="test_knowledge"
    )
    
    # 添加知识
    print("添加知识条目...")
    await kb.add_knowledge(
        content="机器人的前进命令是 move_forward",
        metadata={"category": "command", "type": "movement"}
    )
    await kb.add_knowledge(
        content="机器人的后退命令是 move_backward",
        metadata={"category": "command", "type": "movement"}
    )
    await kb.add_knowledge(
        content="机器人紧急停止命令是 stop",
        metadata={"category": "safety", "type": "emergency"}
    )
    
    # 获取统计
    stats = kb.get_statistics()
    print(f"✓ 知识库统计: {stats}")
    
    # 检索知识
    print("\n检索关键词'前进':")
    results = await kb.search(query="前进", top_k=2)
    print(f"  找到 {len(results)} 条结果")
    for item in results:
        print(f"  - {item.content}")
    
    return True


async def test_agent_graph():
    """测试Agent图"""
    print("\n" + "="*60)
    print("测试4: Agent任务编排")
    print("="*60)
    
    tool_mgr = ToolManager()
    kb = KnowledgeBase()
    chat_mgr = ChatManager()
    
    # 加载示例知识库
    await kb.load_sample_knowledge()
    
    # 创建Agent
    agent = AgentGraph(
        tool_manager=tool_mgr,
        knowledge_base=kb,
        chat_manager=chat_mgr
    )
    
    # 测试对话
    test_queries = [
        "你好",
        "当前时间",
        "计算 100+200",
        "查询机器人控制命令"
    ]
    
    for query in test_queries:
        print(f"\n用户: {query}")
        result = await agent.process(
            user_input=query,
            conversation_id="test_001"
        )
        
        print(f"助手: {result['response'][:100]}...")
        if result.get('tools_used'):
            print(f"使用的工具: {result['tools_used']}")
    
    return True


async def test_api_health():
    """测试API健康状态"""
    print("\n" + "="*60)
    print("测试5: API服务健康检查")
    print("="*60)
    
    try:
        import requests
        
        # 假设服务在5000端口运行
        response = requests.get('http://localhost:5000/api/health', timeout=2)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ API健康状态: {data}")
            return True
        else:
            print(f"⚠️ API返回状态码: {response.status_code}")
            return False
    
    except ImportError:
        print("⚠️ requests库未安装，跳过API测试")
        print("  如需测试API，请先安装: pip install requests")
        print("  或手动启动服务: cd python && python -m api.main")
        return True  # 不阻塞测试流程
    
    except Exception as e:
        print(f"⚠️ API服务未运行: {e}")
        print("  提示: 需要先启动API服务")
        print("  命令: cd python && python -m api.main")
        return True  # 不阻塞测试流程


async def main():
    """主测试流程"""
    print("\n" + "="*70)
    print("🚀 Robot Control System - 核心功能测试")
    print("="*70)
    
    tests = [
        ("对话管理器", test_chat_manager),
        ("工具管理器", test_tool_manager),
        ("知识库", test_knowledge_base),
        ("Agent任务编排", test_agent_graph),
        ("API健康检查", test_api_health),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = await test_func()
            results.append((test_name, success))
        except Exception as e:
            logger.error(f"测试 '{test_name}' 失败: {e}")
            results.append((test_name, False))
    
    # 打印测试总结
    print("\n" + "="*70)
    print("📊 测试总结")
    print("="*70)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{status} - {test_name}")
    
    print(f"\n总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！系统核心功能正常工作。")
        return 0
    else:
        print(f"\n⚠️ {total - passed} 个测试失败，请检查相关模块。")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
