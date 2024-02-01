from bs4 import BeautifulSoup
import requests
import csv
import re


def get_page_info(url):
    page = requests.get(url)
    soup_page = BeautifulSoup(page.content, 'html.parser')
    if "olx" in soup_page:
        same_class = "css-b5m1rv er34gjf0"
        level = soup_page.find('p', class_=same_class, string=re.compile('Poziom'))
        furnit = soup_page.find('p', class_=same_class, string=re.compile('Umeblowane'))
        typeof = soup_page.find('p', class_=same_class, string=re.compile('Rodzaj zabudowy'))
        rooms = soup_page.find('p', class_=same_class, string=re.compile('Liczba pokoi'))
        area = soup_page.find('p', class_=same_class, string=re.compile('Powierzchnia'))
        typeof2 = soup_page.find('p', class_=same_class, string=re.compile('Firmowe|Prywatne'))
        czynsz = soup_page.find('p', class_=same_class, string=re.compile('Czynsz'))

        level_text = level.text.strip()[8:] if level else 'No info'
        furnit_text = furnit.text.strip()[12:] if furnit else 'No info'
        typeof_text = typeof.text.strip()[17:] if typeof else 'No info'
        rooms_text = rooms.text.strip()[14:] if rooms else 'No info'
        area_text = area.text.strip()[14:] if area else 'No info'
        typeof2_text = typeof2.text.strip() if typeof2 else 'No info'
        czynsz_text = czynsz.text.strip() if czynsz else 'No info'

    return level_text, rooms_text, typeof_text, area_text, furnit_text, typeof2_text, czynsz_text

first_page_url = "https://www.olx.pl/nieruchomosci/mieszkania/wynajem/warszawa/#892319577"
page_to_scrape = requests.get(first_page_url)
max_page = soup_page.find('p', class_=same_class)

<li data-testid="pagination-list-item" aria-label="Page 25" tabindex="0" font-size="p3" class="  pagination-item  css-ps94ux"><a data-testid="pagination-link-25" class="css-1mi714g" href="/nieruchomosci/mieszkania/warszawa/?page=25">25</a></li>


with open("scrapped_data.csv", "w", newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["TITLE", "PRICE", "LINK", "LEVEL","NO. ROOMS", "TYPE", "AREA",  "FURNITURE", "TYPEOF2", "CZYNSZ"])

    for page in range(2,26):
        soup = BeautifulSoup(page_to_scrape.content, 'html.parser')
        titles = soup.find_all('h6', class_="css-16v5mdi er34gjf0")
        prices = soup.find_all('p', class_="css-10b0gli er34gjf0")
        listing_urls = [a['href'] for a in soup.find_all('a', class_="css-rc5s2u", href=True)]
        listing_urls = ["https://olx.pl" + url if not url.startswith("http") else url for url in listing_urls]

        for title, price, url in zip(titles, prices, listing_urls):
            title_text = title.text.strip() if title else 'No title'
            price_text = price.text.strip()[:-13].strip() if price and price.text.endswith('do negocjacji') else (
                price.text.strip() if price else 'No price')
            level, rooms, typeof, area, furnit, typeof2, czynsz  = get_page_info(url)

            writer.writerow([title_text, price_text, url, level, rooms, typeof, area, furnit, typeof2, czynsz])
        other_pages = "https://www.olx.pl/nieruchomosci/mieszkania/wynajem/warszawa/" + "?page=" + str(page)
        page_to_scrape = requests.get(other_pages)

    file.close()
# dodaje url, próbuję przyciąć komórki

# https://www.olx.pl/nieruchomosci/mieszkania/wynajem/warszawa/#892319577
# https://www.olx.pl/nieruchomosci/mieszkania/wynajem/warszawa/?page=2
# https://www.olx.pl/nieruchomosci/mieszkania/wynajem/warszawa/?page=3
# okolo 50 ogloszen na kazdej ze stron
