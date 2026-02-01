from bs4 import BeautifulSoup

from webScrapping.selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get("https://ecatalogue.firabarcelona.com/barcelonawineweek2026/home?filter=ONLY_EXHIBITORS&lang=en_GB")

WebDriverWait(driver, 60).until(
    lambda d: d.execute_script("return document.readyState") == "complete"
)

# wait until Angular actually renders something
WebDriverWait(driver, 60).until(
    lambda d: d.execute_script(
        "return document.querySelectorAll('app-root *').length > 0"
    )
)

logs = driver.get_log("browser")
for log in logs:
    print(log)

html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')
# print(soup)
data = soup.find_all('div', attrs={'class':'ex__data'})
print(data)
for d in data:
    print(d.text)

driver.quit()
