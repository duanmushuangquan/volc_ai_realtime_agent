import { SearchClient, Config } from "coze-coding-dev-sdk";
async function main() {
  const config = new Config();
  const client = new SearchClient(config);
  const results = await client.webSearch("OpenClaw 具身智能 gateway memory 记忆 架构设计", 10, true);
  console.log("=== OpenClaw 架构详解 ===");
  if (results.summary) console.log("Summary:", results.summary);
  results.web_items?.forEach((item, i) => {
    console.log(`${i+1}. ${item.title} | ${item.snippet.substring(0, 100)}...`);
  });
}
main().catch(console.error);
