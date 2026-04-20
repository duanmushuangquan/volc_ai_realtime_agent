import { SearchClient, Config } from "coze-coding-dev-sdk";

async function main() {
  const config = new Config();
  const client = new SearchClient(config);
  
  // 搜索火山 ASR TTS
  const results = await client.webSearch("火山引擎 ASR 语音识别 TTS 语音合成 SDK API 2024", 10, true);
  console.log("=== 火山引擎 ASR/TTS ===");
  if (results.summary) console.log("Summary:", results.summary);
  results.web_items?.forEach((item, i) => {
    console.log(`${i+1}. ${item.title}`);
    console.log(`   URL: ${item.url}`);
  });
}

main().catch(console.error);
