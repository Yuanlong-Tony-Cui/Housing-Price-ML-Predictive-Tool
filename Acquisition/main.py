from fb_group_scraper import fb_group_scraper
from fb_group_json import fb_group_json
from address_extractor import address_extractor
from kijiji_html_extractor import extract_kijiji_postings
from OpenAIParser.openai_parser import parse_kijiji_posting
from kijiji_html_extractor import extract_kijiji_postings
import json

ad_links = extract_kijiji_postings()
print(len(ad_links))
print(ad_links)

housing_data = []
for url in ad_links:
    data = parse_kijiji_posting(url)
    if data:
        housing_data.append(data)

with open('housing_data.json', 'w') as f:
    f.write(json.dumps(housing_data))


# # Scrape the fb group by scrolling down x times and expand all "See more" and store as .html
# url = "https://www.facebook.com/groups/110354088989367?locale=en_US"
# html_name = "Acquisition/page.html"
# fb_group_scraper(url, 5, html_name)

# # Parse through the html and read all posting messages and store in .json
# json_name = "Acquisition/page.json"
# fb_group_json(html_name, json_name)

# # Extract addresses from the noisy texts in .json
# addresses = address_extractor(json_name)
# print(addresses)

# ad_postings = extract_kijiji_postings()
