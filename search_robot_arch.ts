import { SearchClient, Config } from "coze-coding-dev-sdk";

async function main() {
  const config = new Config();
  const client = new SearchClient(config);
  
  // 搜索机器人控制系统架构
  const results = await client.webSearch("robot control system architecture DDS WebSocket HTTP communication 2024", 10, true);
  console.log("=== Robot Control System Architecture ===");
  if (results.summary) console.log("Summary:", results.summary);
  results.web_items?.forEach((item, i) => {
    console.log(`${i+1}. ${item.title}`);
    console.log(`   URL: ${item.url}`);
  });
}

main().catch(console.error);
