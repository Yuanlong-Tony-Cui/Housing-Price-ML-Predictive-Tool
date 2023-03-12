from bs4 import BeautifulSoup
import json

def fb_group_json(html_name,json_name):

    # Load the HTML file
    with open(html_name, encoding="utf8") as f:
        html = f.read()

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Find all the span elements with the xtvhhri class
    spans = soup.find_all("span", class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h")

    texts = [span.get_text() for span in spans]
    data = {"texts": texts}
    with open(json_name, "w") as outfile:
        # Write the JSON object to the file
        json.dump(data, outfile)
