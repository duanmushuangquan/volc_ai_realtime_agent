import { SearchClient, Config } from "coze-coding-dev-sdk";
async function main() {
  const config = new Config();
  const client = new SearchClient(config);
  const results = await client.webSearch("实时语音 端到端延迟 优化 架构 2024 500ms", 10, true);
  console.log("=== 实时语音延迟优化 ===");
  if (results.summary) console.log("Summary:", results.summary);
  results.web_items?.forEach((item, i) => {
    console.log(`${i+1}. ${item.title} | ${item.snippet.substring(0, 100)}...`);
  });
}
main().catch(console.error);
