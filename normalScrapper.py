from bs4 import BeautifulSoup, NavigableString
from urllib.request import urlopen
import certifi
import ssl

# Create an SSL context with certifi's CA bundle
# ssl_context = ssl.create_default_context(cafile=certifi.where())
url = 'https://erevuka.org/page/courses'

path = urlopen(url)

body_bytes = path.read()
data = body_bytes.decode('utf-8')

soup = BeautifulSoup(data,'html.parser')
pages = soup.find_all(class_='page-item')
# print(pages)
pager = []
courses = {}

for i, page in enumerate(pages):
    #convert string to int if <  or > skipp
    try:
    #  page.text = int(page.text)
     pager.append(int(page.text))
    except:
        # print('cannot convert')
        pass


def openPages(number):
   page = url +"?page={}".format(number) 
   path = urlopen(page)
   body_bytes = path.read()
   data = body_bytes.decode('utf-8')
   soup = BeautifulSoup(data, 'html.parser')
   """ extract course cards"""
   cards = soup.find_all(class_='course-card-content')
   return cards

while pager:
   first = pager.pop(0)
   batches = openPages(first)
   coursesInBatch = []
   for card in batches:
      coursesInBatch.append(card.find(class_='title-span').text)
#    break
   courses.update({f'page {first}': coursesInBatch})

for course in courses:
    print(course)
    print('\n')
    for value in courses[course]:
       print(value)
    print('\n')


