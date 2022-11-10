import time
import requests
from bs4 import BeautifulSoup
import json

categories = {
    "air-jordan": ["4", "5", "6", "7", "8", "9", "10", "11", "12", "13"],
    "nike": ["air-force", "kobe", "lebron", "dunk", "sb", "sacai", "yeezy", "blazer", "cortez"]}  # all the categories
# of shoes on StockX
years = list(range(2001, 2022))  # creates a range of all the years on StockX website

shoes = []  # added shoes
page = 1  # starting page number

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:24.0) Gecko/20100101 Firefox/24.0'}
# user agent, need to change once in a while to avoid blocking at https://developers.whatismybrowser.com/useragents/explore/software_name/chrome/

for category in categories:  # iterate over category array
    for subcat in categories[category]:  # subcategory in category
        for year in years:  # iterates over the years
            while (page <= 25):  # go through 25 pages everytime
                time.sleep(35)  # sleep to avoid beig flagged and blocked
                print(f'Page {page}, year: {year}, category: {category}, subcategory: {subcat}')

                if category == 'air-jordan':
                    url = f'https://stockx.com/retro-jordans/{category}-{subcat}?years={year}&page={page}'  # link setup
                else:
                    url = f'https://stockx.com/{category}/{subcat}?years={year}&page={page}'

                response = requests.get(url, headers=headers)  # send html request

                soup = BeautifulSoup(response.text, 'html.parser')  # parse data
                soup = soup.find("div", id="browse-wrapper")
                data = json.loads(
                    "".join(soup.find("script", {"type": "application/ld+json"}).contents))  # gets specific header

                for x in data["itemListElement"]:
                    try:
                        test = x["item"]['sku']  # sees if there is any data on the page

                        data = {
                            "name": x["item"]["name"],
                            "url": x["item"]["url"]
                        }
                        shoes.append(x["item"]['name'])
                    except:
                        test = 0
                        page = 26  # makes page over 26 to go to another year or category
                page += 1
            page = 1
