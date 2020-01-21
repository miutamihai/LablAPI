import requests
from lxml import html

from getProps import get_headers


def get_average_price(beer_name, country):
    page = requests.get('https://www.wine-searcher.com/find/' + beer_name + '/1/' + country,
                        headers=get_headers())
    tree = html.fromstring(page.content)
    average_price = tree.xpath('//div[1]/div[2]/div/div[2]/div/div/div/div[3]/div/div/div[1]/div/div['
                               '2]/span[2]/b/text()')
    return average_price[0]
