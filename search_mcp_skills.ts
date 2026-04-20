import { SearchClient, Config } from "coze-coding-dev-sdk";
async function main() {
  const config = new Config();
  const client = new SearchClient(config);
  const results = await client.webSearch("MCP Model Context Protocol Skills 机器人 function call 2024 2025", 10, true);
  console.log("=== MCP Skills FunctionCall ===");
  if (results.summary) console.log("Summary:", results.summary);
  results.web_items?.forEach((item, i) => {
    console.log(`${i+1}. ${item.title} | ${item.snippet.substring(0, 100)}...`);
  });
}
main().catch(console.error);
