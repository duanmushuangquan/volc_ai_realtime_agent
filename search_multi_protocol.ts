import { SearchClient, Config } from "coze-coding-dev-sdk";

async function main() {
  const config = new Config();
  const client = new SearchClient(config);
  
  // 搜索多协议通信架构
  const results = await client.webSearch("robot multi protocol DDS HTTP WebSocket ROS2 communication architecture", 10, true);
  console.log("=== Multi-Protocol Communication ===");
  if (results.summary) console.log("Summary:", results.summary);
  results.web_items?.forEach((item, i) => {
    console.log(`${i+1}. ${item.title}`);
    console.log(`   URL: ${item.url}`);
  });
}

main().catch(console.error);
