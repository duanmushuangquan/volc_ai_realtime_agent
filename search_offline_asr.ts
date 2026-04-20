import { SearchClient, Config } from "coze-coding-dev-sdk";
async function main() {
  const config = new Config();
  const client = new SearchClient(config);
  const results = await client.webSearch("FunASR 语音识别 离线部署 2024 最新进展", 10, true);
  console.log("=== FunASR 离线部署 ===");
  if (results.summary) console.log("Summary:", results.summary);
  results.web_items?.forEach((item, i) => {
    console.log(`${i+1}. ${item.title} | ${item.url}`);
  });
}
main().catch(console.error);
