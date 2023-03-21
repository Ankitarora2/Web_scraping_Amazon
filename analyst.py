import requests
from bs4 import BeautifulSoup
import csv

# Define the url to scrape
base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{}'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# Number of pages to scrape
num_pages = 20

# The list to store the scraped data
products = []

# Scrape information for each product
for i in range(1, num_pages + 1):
    url = base_url.format(i)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    product_list = soup.find_all('div', {'data-component-type': 's-search-result'})

    # Loop through each product and scrape its information
    for product in product_list:
        try:
            product_url = 'https://www.amazon.in' + product.find('a', {'class': 'a-link-normal s-no-outline'})['href']
            product_name = product.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).text.strip()
            product_price = product.find('span', {'class': 'a-price-whole'}).text.strip()
            product_rating = product.find('span', {'class': 'a-icon-alt'}).text.strip().split()[0]
            product_num_reviews = product.find('span', {'class': 'a-size-base'}).text.strip().split()[0]

            # Follow the url to the product page and scrape extra information
            response = requests.get(product_url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            product_description = soup.find('div', {'id': 'productDescription'}).text.strip()
            product_asin = soup.find('input', {'id': 'ASIN'})['value']
            product_manufacturer = soup.find('a', {'id': 'bylineInfo'})['href'].split('/')[1]

            # Store the scraped data for each product in a dictionary and add it to the list
            product_dict = {'Product URL': product_url, 'Product Name': product_name, 'Product Price': product_price,
                            'Rating': product_rating, 'Number of Reviews': product_num_reviews,
                            'Description': product_description,
                            'ASIN': product_asin, 'Manufacturer': product_manufacturer}
            products.append(product_dict)

        except:
            pass

# Write the scraped data to a CSV file
with open('amazon_products.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=products[0].keys())
    writer.writeheader()
    for product in products:
        writer.writerow(product)
print('Scraping completed successfully!')
