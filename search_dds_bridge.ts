import { SearchClient, Config } from "coze-coding-dev-sdk";
async function main() {
  const config = new Config();
  const client = new SearchClient(config);
  const results = await client.webSearch("Fast DDS ROS2 bridge 非ROS系统 通信桥接", 10, true);
  console.log("=== DDS 桥接方案 ===");
  if (results.summary) console.log("Summary:", results.summary);
  results.web_items?.forEach((item, i) => {
    console.log(`${i+1}. ${item.title} | ${item.snippet.substring(0, 100)}...`);
  });
}
main().catch(console.error);
