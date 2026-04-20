import { SearchClient, Config } from "coze-coding-dev-sdk";

async function main() {
  const config = new Config();
  const client = new SearchClient(config);
  
  // 搜索 Isaac Sim 机器人仿真
  const results = await client.webSearch("Isaac Sim ROS2 robot simulation integration 2024", 10, true);
  console.log("=== Isaac Sim Robot Simulation ===");
  if (results.summary) console.log("Summary:", results.summary);
  results.web_items?.forEach((item, i) => {
    console.log(`${i+1}. ${item.title}`);
    console.log(`   URL: ${item.url}`);
  });
}

main().catch(console.error);
