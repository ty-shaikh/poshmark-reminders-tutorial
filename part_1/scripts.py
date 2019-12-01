# Imports
from requests import get
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import datetime, timedelta
import pickle

# Constants
SEARCH_URL = "https://poshmark.com/brand/Naked_&_Famous_Denim-Men-Jeans?sort_by=added_desc"
HEADER = { 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
DAYS = 4

# Download and parse Poshmark listings
def run_search(search_url):
    "Pull down search results and extract out product cards"
    response = get(search_url, headers=HEADER)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    item_container = html_soup.find_all('div', class_ = 'tile')

    return item_container

product_cards = run_search(SEARCH_URL)
# print(product_cards)

# Extract product listing attributes
def get_attributes(soup_obj):
    "Extract product values from card"
    price = soup_obj['data-post-price']

    url_tag = soup_obj.a
    url = "https://poshmark.com" + url_tag['href']
    title = url_tag['title']

    img_tag = url_tag.img
    img = img_tag['src']

    return (title, price, url, img)

first_card = product_cards[0]
card_attributes = get_attributes(first_card)
# print('Title: ', card_attributes[0])
# print('Price: ', card_attributes[1])
# print('Link: ', card_attributes[2])
# print('Image: ', card_attributes[3])

# Calculate the time difference
def get_days(soup_obj):
    "Convert to EST and return difference in days"
    created_date = soup_obj['data-created-at']

    pst_date = parse(created_date, ignoretz=True)
    est_date = pst_date + timedelta(hours=3)

    now = datetime.now()
    diff = abs((est_date-now).days)

    return diff

days = get_days(first_card)
# print(days)

# Find recent items
recent_items = []

for card in product_cards:
    difference = get_days(card)

    if difference <= DAYS:
        card_values = get_attributes(card)
        recent_items.append(card_values)
    else:
        break

summary = f'Found {len(recent_items)} items posted in the last {DAYS} days'
print(summary)
print('')

for item in recent_items:
    print('Title: ', item[0])
    print('Price: ', item[1])
    print('Link: ', item[2])
    print('')

pickle.dump(recent_items, open("naked_and_famous.p", "wb"))
