# import the necessary libraries
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm


def extract_kijiji_postings():
    # Declaring page number and total pages
    page_number = 1
    total_pages = 58
    ad_links = []
    # base URL for the Kijiji website
    base_url = "https://www.kijiji.ca"

    print("Extracting Kijiji Links")
    for i in tqdm(range(total_pages)):
        # URL for the first page
        page_1_url = base_url + '/b-for-rent/city-of-toronto/rental/k0c30349001l1700273?ll=43.662892%2C-79.395656&address=University+of+Toronto%2C+King%26%2327%3Bs+College+Circle%2C+Toronto%2C+ON&radius=9.0'
        previous_page = 'page-' + str(page_number - 1)
        current_page = 'page-' + str(page_number)
        page_1_url.replace(previous_page, current_page)
        # use requests library to get respo
        response = requests.get(page_1_url)

        # use BS to parse the text of the HTML response
        soup = BeautifulSoup(response.text, "lxml")

        # find all of the relevant ads
        ads = soup.find_all(
            "div", attrs={"class": ["search-item", "regular-ad"]})

        # removes marketing / third party ads
        ads = [x for x in ads if (
            "cas-channel" not in x["class"]) & ("third-party" not in x["class"])]

        # create a list to store all of the URLs from the

        for ad in ads:
            # parse the link from the ad
            link = ad.find_all("a", {"class": "title"})
            # add the link to the list
            for l in link:
                ad_links.append(base_url + l["href"])
        page_number += 1

    with open('kijiji_links.txt', 'w') as f:
        for item in ad_links:
            f.write("%s\n" % item)

    print(f"Found {len(ad_links)} urls from Kijiji")
    return ad_links


# extract_kijiji_postings()
