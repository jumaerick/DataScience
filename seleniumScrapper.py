from bs4 import BeautifulSoup, NavigableString
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get("https://www.rottentomatoes.com/")

html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

body = soup.find('body')

# print(body.get('iframe'))
# button = soup.find('button', attrs={'data-type': 'Movie'})
# par = button.parent.find('div', class_ = 'dynamic-poster-list__sponsored-header')

# par = ''
# print(par)

#Extracting trailers with title and descriptions
# trailers = soup.find_all(attrs={'trailers-and-videos-item'})
# for trailer in trailers:
#     print("{:<10} | {:<10}".format('Title', 'Description'))
#     print("{:<10} | {:<10}".format(trailer.find('h3').text, trailer.find('p').text)) # Left-aligns with 10 spaces

#comming soon to theatre
# soon = soup.find_all('h2', attrs={'class': 'unset', 'data-qa': 'title'})
divers = soup.find_all(class_='dynamic-poster-list')
# print(len(divers))
access = True
for diver in divers:
    #fetching class that start with
    header = diver.find(class_= re.compile('dynamic-poster-list__header-container'))
    with open('test.csv', '+a') as openfile:
        title = header.find('h2', attrs={'data-qa':'title'}).text
        openfile.write(title +'\n')
        
    # print(header.find('h2', attrs={'data-qa':'title'}).text)

    tilesCarousel = diver.find_all('tiles-carousel-responsive-item-deprecated')
    print('Movies Count', len(tilesCarousel))

    for tile in tilesCarousel:
        with open('test.csv', 'a+') as openfile:
            tileTitle = tile.find('watchlist-button')['media-title']
            openfile.write(tileTitle +'\n')
        # print(tile.find('watchlist-button')['media-title'])
    # print(tilesCarousel.find('button', attrs = {'data-type': 'Movie'}).text)
# allTiles = tilesCarousel.find_all('tiles-carousel-responsive-item-deprecated')
# for tile in allTiles:
#     print(tile)
# for child in diver.children:
#     print(child)
# for item in soon:
#     print('hapa')
    # items = item.find_all('button', attrs={'data-type':'Movie'})
    # print('Number of items', len(items))
# print(soon)
# found = False
# for parent in button.parents:

#     nps = parent.find('h2', attrs={'class': 'unset', 'data-qa': 'title'})
#     if(nps):
#         par = nps.text
#         break
#     else:
#         pass
#         print(parent)


# print(par)

# for p in soup.find_all('button', attrs={'data-type': 'Movie'}):
#     print(p.get('data-title'))
driver.quit()
