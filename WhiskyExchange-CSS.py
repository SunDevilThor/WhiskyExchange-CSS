# WhiskyExchange - Using CSS Selectors
# Tutorial from John Watson Rooney YouTube channel

import requests
from bs4 import BeautifulSoup
import pandas as pd
from itertools import chain

def get_page_links(url):
    base_url = 'https://www.thewhiskyexchange.com'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    links = soup.select('li.product-grid__item a')
    return [base_url + link.attrs['href'] for link in links]

def product_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    product = {
        'title': soup.select_one('h1.product-main__name').text.strip().replace('\n', ' '),
        'price': soup.select_one('p.product-action__price').text.strip().replace('\n', ''),
        'availability': soup.select_one('p.product-action__stock-flag').text.strip().replace('\n', ''),
        'info': soup.select_one('p.product-main__data').text.strip().replace('\n', ''),
        #'origin': soup.select_one('ul.product-main__meta').text.strip().replace('\n', ''),
    }

    return product

def main(): 
    results = []
    for x in range(1, 3):
        urls = get_page_links(f'https://www.thewhiskyexchange.com/c/305/rest-of-the-world-whisky?pg={x}&psize=120&sort=pasc')
        product_info = [product_data(url) for url in urls]
        results.append(product_info)
        print(f'Page {x} completed.')
    return results

main()

df = pd.DataFrame(list(chain.from_iterable(main())))
df.to_csv('Whisky-CSS.csv', index=False)
print('Saved items to CSV file.')

# To- DO: 
# Fix Origin
# Change page size from 120 to 24
