# Imports
from requests import get
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import datetime, timedelta

# Constants
HEADER = { 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

# Download and parse Poshmark listings
def run_search(search_url):
    "Pull down search results and extract out product cards"
    response = get(search_url, headers=HEADER)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    item_container = html_soup.find_all('div', class_ = 'tile')

    return item_container

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

# Calculate the time difference
def get_days(soup_obj):
    "Convert to EST and return difference in days"
    created_date = soup_obj['data-created-at']

    pst_date = parse(created_date, ignoretz=True)
    est_date = pst_date + timedelta(hours=3)

    now = datetime.now()
    diff = abs((est_date-now).days)

    return diff
