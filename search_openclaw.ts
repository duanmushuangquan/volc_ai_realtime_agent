import { SearchClient, Config } from "coze-coding-dev-sdk";

async function main() {
  const config = new Config();
  const client = new SearchClient(config);
  
  // 搜索 openclaw
  const results = await client.webSearch("openclaw robotics tier4 robot control system DDS", 10, true);
  console.log("=== OpenClaw Robotics ===");
  if (results.summary) console.log("Summary:", results.summary);
  console.log("Results count:", results.web_items?.length || 0);
  results.web_items?.forEach((item, i) => {
    console.log(`${i+1}. ${item.title}`);
    console.log(`   URL: ${item.url}`);
    console.log(`   Snippet: ${item.snippet.substring(0, 150)}...`);
  });
}

main().catch(console.error);
