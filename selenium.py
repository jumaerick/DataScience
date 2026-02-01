from bs4 import BeautifulSoup, NavigableString

from webScrapping.selenium import webdriver
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
button = soup.find('button', attrs={'data-type': 'Movie'})
# par = button.parent.find('div', class_ = 'dynamic-poster-list__sponsored-header')

par = ''
# print(par)

found = False
for parent in button.parents:

    nps = parent.find('h2', attrs={'class': 'unset', 'data-qa': 'title'})
    if(nps):
        par = nps.text
        break
    else:
        pass
        print(parent)


print(par)

# for p in soup.find_all('button', attrs={'data-type': 'Movie'}):
#     print(p.get('data-title'))
driver.quit()
