import openai
import configparser
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import json
import os

config = configparser.ConfigParser()
dir = os.path.dirname(os.path.abspath(__file__))
config.read_file(open(os.path.join(dir, 'openai.config')))
API_KEY = config.get('API KEY', 'API_KEY')
openai.api_key = API_KEY


def parse_kijiji_posting(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

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
            - utilities_included: bool, if hydro, wifi, water and heating is included then this field is true, else it's false.
            - in_unit_laundry: bool, if there is laundry in unit. If undeterminable, assume false
            - gym: bool, if there is a gym in the building. If undeterminable, assume false.
            - parking: bool, if the unit has parking available.
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
    print(chatCompletion['choices'][0]['message']['content'])
    try:
        output = json.loads(chatCompletion['choices'][0]['message']['content'])
    except:
        print('Did not receive a valid JSON')

    return output
