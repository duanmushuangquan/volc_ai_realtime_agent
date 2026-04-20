import { SearchClient, Config } from "coze-coding-dev-sdk";
async function main() {
  const config = new Config();
  const client = new SearchClient(config);
  const results = await client.webSearch("火山引擎 豆包 离线私有化部署 edge 边缘部署 2024 2025", 10, true);
  console.log("=== 火山离线方案 ===");
  if (results.summary) console.log("Summary:", results.summary);
  results.web_items?.forEach((item, i) => {
    console.log(`${i+1}. ${item.title} | ${item.snippet.substring(0, 100)}...`);
  });
}
main().catch(console.error);
