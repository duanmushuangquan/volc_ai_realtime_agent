import { SearchClient, Config } from "coze-coding-dev-sdk";

async function main() {
  const config = new Config();
  const client = new SearchClient(config);
  
  // 搜索火山引擎 RTC
  const rtcResults = await client.webSearch("火山引擎 RTC SDK C++ Linux 实时音视频", 10, true);
  console.log("=== 火山引擎 RTC ===");
  if (rtcResults.summary) console.log("Summary:", rtcResults.summary);
  console.log("Results count:", rtcResults.web_items?.length || 0);
  rtcResults.web_items?.forEach((item, i) => {
    console.log(`${i+1}. ${item.title}`);
    console.log(`   URL: ${item.url}`);
    console.log(`   Snippet: ${item.snippet.substring(0, 100)}...`);
  });
}

main().catch(console.error);
