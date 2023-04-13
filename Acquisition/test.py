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
