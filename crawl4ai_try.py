import os
import json
import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import LLMExtractionStrategy


async def extract_tech_content():
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(
            url="https://mzh.moegirl.org.cn/MyGO!!!!!",
            extraction_strategy=LLMExtractionStrategy(
                provider="openai/glm-4-flash",
                base_url="https://open.bigmodel.cn/api/paas/v4",
                instruction="总结乐队成员的性格和一些趣事",
                api_token="",
                verbose=True
            ),
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
            bypass_cache=True,
        )
        # 数据非法，难绷

    tech_content = json.loads(result.extracted_content)
    print(f"Number of tech-related items extracted: {len(tech_content)}")

    with open("./raw_data/tech_summaries.json", "w", encoding="utf-8") as f:
        json.dump(tech_content, f, indent=2)

asyncio.run(extract_tech_content())
