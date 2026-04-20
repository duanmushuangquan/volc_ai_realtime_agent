import { SearchClient, Config } from "coze-coding-dev-sdk";
async function main() {
  const config = new Config();
  const client = new SearchClient(config);
  const results = await client.webSearch("Qwen-Audio 阿里通义 语音模型 离线部署 2024 2025", 10, true);
  console.log("=== Qwen Audio 语音模型 ===");
  if (results.summary) console.log("Summary:", results.summary);
  results.web_items?.forEach((item, i) => {
    console.log(`${i+1}. ${item.title} | ${item.url}`);
  });
}
main().catch(console.error);
