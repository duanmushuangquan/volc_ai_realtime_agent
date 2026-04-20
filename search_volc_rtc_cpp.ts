import { SearchClient, Config } from "coze-coding-dev-sdk";

async function main() {
  const config = new Config();
  const client = new SearchClient(config);
  
  // 搜索火山 RTC C++ SDK
  const results = await client.webSearch("火山引擎 RTC C++ SDK 下载 GitHub Linux demo", 10, true);
  console.log("=== 火山 RTC C++ SDK ===");
  if (results.summary) console.log("Summary:", results.summary);
  results.web_items?.forEach((item, i) => {
    console.log(`${i+1}. ${item.title}`);
    console.log(`   URL: ${item.url}`);
    console.log(`   Snippet: ${item.snippet.substring(0, 100)}...`);
  });
}

main().catch(console.error);
