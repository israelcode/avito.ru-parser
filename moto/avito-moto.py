import requests
from bs4 import BeautifulSoup
import csv
import time 
 
def get_html(url):
    r = requests.get(url)
    return r.text
 
 
def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find('div', class_='pagination-pages clearfix')
    pages = divs.find_all('a', class_='pagination-page')[-1].get('href')
    total_pages = pages.split('=')[1].split('&')[0]
    return int(total_pages)
 
 
def write_csv(data):
    with open('moto.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['title'],
                         data['price'],
                         data['text'],
                         data['url']))
 
 
def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find('div', class_='catalog-list')
    ads = divs.find_all('div', class_='item_table')

    for ad in ads:
        try:
            div = ad.find('div', class_='description').find('h3')
            title = div.text.strip()

        except:
            title = ''
        try:
            div = ad.find('div', class_='description').find('h3')
            url = "https://avito.ru" + div.find('a').get('href')
        except:
            url = ''
        try:
            price = ad.find('span', class_='price').text.strip()
        except:
            price = ''
        try:
            #div = ad.find('div', class_='data')
            text = ad.find('div', class_='specific-params').text.strip()
        except:
            text = ''
        data = {'title':title,
                'price':price,
                'text':text,
                'url':url}
        write_csv(data)
 
 
def main():
    url = 'https://www.avito.ru/moskva/mototsikly_i_mototehnika?p=1&radius=200&i=1'
    base_url = 'https://www.avito.ru/moskva/mototsikly_i_mototehnika?'
    page_part = 'p='
    query_part = '&radius=200&i=1'

 
    # total_pages = get_total_pages(get_html(url))
 
    for i in range(89, 100):
        url_gen = base_url + page_part + str(i) + query_part
        print(url_gen)
        html = get_html(url_gen)
        get_page_data(html)
 
 
if __name__ == '__main__':
    main()
