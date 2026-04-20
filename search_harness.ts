import { SearchClient, Config } from "coze-coding-dev-sdk";

async function main() {
  const config = new Config();
  const client = new SearchClient(config);
  
  // 搜索 OpenClaw harness
  const results = await client.webSearch("OpenClaw harness robot VLA embodied AI NVIDIA 2024", 10, true);
  console.log("=== OpenClaw Harness ===");
  if (results.summary) console.log("Summary:", results.summary);
  results.web_items?.forEach((item, i) => {
    console.log(`${i+1}. ${item.title}`);
    console.log(`   URL: ${item.url}`);
    console.log(`   Snippet: ${item.snippet.substring(0, 150)}...`);
  });
}

main().catch(console.error);
