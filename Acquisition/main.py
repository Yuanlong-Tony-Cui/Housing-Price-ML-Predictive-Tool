from fb_group_scraper import fb_group_scraper
from fb_group_json import fb_group_json
from address_extractor import address_extractor

# Scrape the fb group by scrolling down x times and expand all "See more" and store as .html
url = "https://www.facebook.com/groups/110354088989367?locale=en_US"
html_name = "Acquisition/page.html"
fb_group_scraper(url,5,html_name)

# Parse through the html and read all posting messages and store in .json
json_name = "Acquisition/page.json"
fb_group_json(html_name,json_name)

# Extract addresses from the noisy texts in .json
addresses = address_extractor(json_name)
print(addresses)
