import openai
import configparser
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import json

config = configparser.ConfigParser()
config.read_file(open(r'openai.config'))
API_KEY = config.get('API KEY', 'API_KEY')
openai.api_key = API_KEY

# url = 'https://kijiji.ca/v-room-rental-roommate/kitchener-waterloo/private-room-for-rent/1652905554'
url = 'https://www.facebook.com/marketplace/item/1322521661929013/?ref=browse_tab&referral_code=marketplace_general&referral_story_type=general&tracking=%7B%22qid%22%3A%22-4440720341811433459%22%2C%22mf_story_key%22%3A%2234708724068638801%22%2C%22commerce_rank_obj%22%3A%22%7B%5C%22target_id%5C%22%3A34708724068638801%2C%5C%22target_type%5C%22%3A6%2C%5C%22primary_position%5C%22%3A5%2C%5C%22ranking_signature%5C%22%3A6728527316743356416%2C%5C%22commerce_channel%5C%22%3A501%2C%5C%22value%5C%22%3A0.0014512305393326%2C%5C%22upsell_type%5C%22%3A123%2C%5C%22candidate_retrieval_source_map%5C%22%3A%7B%5C%229102763019798296%5C%22%3A801%2C%5C%225979453902171604%5C%22%3A701%2C%5C%229132531913455750%5C%22%3A801%2C%5C%225883461588407502%5C%22%3A801%2C%5C%225934913709927372%5C%22%3A3016%2C%5C%226499594040052137%5C%22%3A801%7D%2C%5C%22grouping_info%5C%22%3Anull%7D%22%2C%22lightning_feed_qid%22%3A%22-4440721716171073194%22%2C%22lightning_feed_ranking_signature%22%3A%226728527316743356416%22%2C%22ftmd_400706%22%3A%22111112l%22%7D'


def parseKijiji(response):
    soup = BeautifulSoup(response.content, 'html.parser')

    # remove unwanted elements
    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text('\n')
    text = " ".join(text.split())
    print(text)

    # gpt-3.5-turbo: $0.002 / 1K tokens generated
    chatCompletion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": """You are a data parser for real estate.
            Given an ambiguous blob of text scraped from the web, you will extract and return in JSON format the following fields:
            - address: string, Canadian address in this format: Address, City, Province 
            - rent: float, rent price in Candian Dollars
            - num_bedrooms: int, number of bedrooms
            - num_bathrooms: int, number of bathrooms
            - furnished: bool, if the unit comes furnished
            - utilities_included: bool, if hydro, wifi, water, heating is included
            - in_unit_laundry: bool, if there is laundry in unit
            - gym: bool, if there is a gym in the building
            - parking: bool, if the unit has parking available
            - female_only: bool, if the unit is female only
            - area: int, area of unit in square foot
            
            If there are fields that are unavailble, then mark them as null."""},
            {"role": "user", "content": text},
        ]
    )

    output = {}
    try:
        output = json.loads(chatCompletion['choices'][0]['message']['content'])
    except:
        print('Did not receive a valid JSON')

    return output


def parseFBMarketplace(response):
    soup = BeautifulSoup(response.content, 'html.parser')

    # remove unwanted elements
    for script in soup(["script", "style", "link"]):
        script.extract()

    text = soup.find('body').get_text()
    metas = soup.find_all('meta', {'name': 'DC.description'})

    for m in metas:
        if m['content']:
            text += f"\n{m['content']}"

    print(text)

    # gpt-3.5-turbo: $0.002 / 1K tokens generated
    chatCompletion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": """You are a data parser for real estate. Only return in JSON format.
            Given an ambiguous blob of text scraped from the web, you will extract and return in JSON format the following fields:
            - address: string, Canadian address in this format: Address, City, Province
            - rent: float, rent price in Candian Dollars
            - num_bedrooms: int, number of bedrooms
            - num_bathrooms: int, number of bathrooms
            - furnished: bool, if the unit comes furnished
            - utilities_included: bool, if hydro, wifi, water, heating is included
            - in_unit_laundry: bool, if there is laundry in unit
            - gym: bool, if there is a gym in the building
            - parking: bool, if the unit has parking available
            - female_only: bool, if the unit is female only
            - area: int, area of unit in square foot

            If there are fields that are unavailble, then mark them as null.
            If the sample text is empty or, there arent enough information, return an empty JSON"""},
            {"role": "user", "content": text},
        ]
    )

    output = {}
    try:
        output = json.loads(chatCompletion['choices'][0]['message']['content'])
    except:
        print('Did not receive a valid JSON')

    return output


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

response = requests.get(url, headers=headers)
print(parseFBMarketplace(response))
