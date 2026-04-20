import { SearchClient, Config } from "coze-coding-dev-sdk";
async function main() {
  const config = new Config();
  const client = new SearchClient(config);
  const results = await client.webSearch("语音到语音 S2S 端到端 离线部署 2024 2025 openai speech-to-speech", 10, true);
  console.log("=== S2S 端到端语音 ===");
  if (results.summary) console.log("Summary:", results.summary);
  results.web_items?.forEach((item, i) => {
    console.log(`${i+1}. ${item.title} | ${item.url}`);
  });
}
main().catch(console.error);
