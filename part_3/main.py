# Import packages and functions from local scripts
import pickle
from scraping import run_search, get_attributes, get_days
from mailer import generate_markup, send_email

# Constant variables
SEARCH_URL = "https://poshmark.com/brand/Naked_&_Famous_Denim-Men-Jeans?sort_by=added_desc"
DAYS = 4
USER_EMAIL = "PERSONAL_ACCOUNT@gmail.com"

# Scrape product cards
product_cards = run_search(SEARCH_URL)

# Find recent items
recent_items = []

for card in product_cards:
    difference = get_days(card)

    if difference <= DAYS:
        card_values = get_attributes(card)
        recent_items.append(card_values)
    else:
        break

# Print summary
summary = f'Found {len(recent_items)} items posted in the last {DAYS} days'
print(summary)

# Export processed data
pickle.dump(recent_items, open("naked_and_famous.p", "wb"))

# Generate markup
email_markup = generate_markup("Naked and Famous Jeans", recent_items)

# Send email
send_email(email_markup, USER_EMAIL)
