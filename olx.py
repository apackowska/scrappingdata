

from bs4 import BeautifulSoup
import requests
import csv
import re


page_to_scrape = requests.get("https://www.olx.pl/nieruchomosci/mieszkania/wynajem/warszawa/?search%5Bprivate_business%5D=private&view=list#676689944")
soup = BeautifulSoup(page_to_scrape.content, 'html.parser')

file = open("scrapped_data.csv", "w", newline='')
writer = csv.writer(file)
writer.writerow(["TITLE", "PRICE", "LINK", "LOCATION", "LEVEL", "AREA", "NO. ROOMS"])


titles = soup.find_all('h6', class_="css-16v5mdi er34gjf0")
prices = soup.find_all('p', class_="css-10b0gli er34gjf0")


listing_urls = [a['href'] for a in soup.find_all('a', class_="css-rc5s2u", href=True)]
listing_urls = ["https://olx.pl" + url if not url.startswith("http") else url for url in listing_urls]



# for title in titles:
#     title_str = str(title)
#     index = title_str.find("</h6>")
#     print(title_str[33:index])

def page_info():
    levels_list = []
    areas_list = []
    furnit_list = []
    type_list = []
    rooms_list = []
    for url in listing_urls:
        page = requests.get(url)
        soup_page = BeautifulSoup(page.content, 'html.parser')
        level = soup_page.find('p', class_="css-b5m1rv er34gjf0", string= re.compile('Poziom'))
        levels_list.append(level.text.strip()) if level else 'No info'
        furnit = soup_page.find('p', class_="css-b5m1rv er34gjf0", string= re.compile('Umeblowane'))
        furnit_list.append(furnit.text.strip()) if furnit else 'No info'
        typeof = soup_page.find('p', class_="css-b5m1rv er34gjf0", string= re.compile('Rodzaj zabudow'))
        type_list.append(typeof.text.strip()) if typeof else 'No info'
        rooms = soup_page.find('p', class_="css-b5m1rv er34gjf0", string= re.compile('Liczba pokoi'))
        rooms_list.append(rooms.text.strip()) if rooms else 'No info'
        area = soup_page.find('p', class_="css-b5m1rv er34gjf0", string= re.compile('Powierzchnia'))
        areas_list.append(area.text.strip()) if area else 'No info'
    return levels_list, rooms_list, type_list, areas_list, furnit_list

for levels, rooms, types, areas, furnit in page_info():
    writer.writerow([levels, rooms, types, areas, furnit])

file.close()

# for title, price, location, level, area, room in zip(titles, prices, locations, levels, areas, rooms):

# for title, price, link in zip(titles, prices,listing_urls):
#     title_text = title.text.strip() if title else 'No title'
#     price_text = price.text.strip()[:-13].strip() if price and price.text.endswith('do negocjacji') else (price.text.strip() if price else 'No price')
#     writer.writerow([title_text, price_text, link])

    # writer.writerow([title_text, price_text, location_text, level_text, area_text, room_text])


