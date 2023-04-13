from fb_group_scraper import fb_group_scraper
from fb_group_json import fb_group_json
from address_extractor import address_extractor
from kijiji_html_extractor import extract_kijiji_postings
from OpenAIParser.openai_parser import parse_kijiji_posting
from kijiji_html_extractor import extract_kijiji_postings
from tqdm import tqdm
import json
import asyncio
import argparse
import os
import time


async def main():
    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip_urls", action="store_true",
                        help="Skip extracting urls from Kijiji and use existing file")
    args = parser.parse_args()
    print(args)
    if not args.skip_urls:
        ad_links = extract_kijiji_postings()
    else:
        print("Skipping URL Extraction, reading from kijiji_links.txt")

        dir = os.path.dirname(os.path.abspath(__file__))

        with open(os.path.join(dir, 'kijiji_links.txt'), 'r') as f:
            ad_links = [line.strip() for line in f.readlines()]

    housing_data = []

    print(f"Processing {len(ad_links)} URLS")
    tasks = []
    for url in ad_links:
        task = asyncio.create_task(parse_kijiji_posting(url))
        tasks.append(task)
        await asyncio.sleep(3)

    results = await asyncio.gather(*tasks)
    for result in results:
        if result:
            housing_data.append(result)

    with open('housing_data.json', 'w') as f:
        f.write(json.dumps(housing_data, indent=4))

    end_time = time.time()

    print(
        f"Runtime: {end_time - start_time:.2f} seconds. Found {len(housing_data)} addresses")


asyncio.run(main())
