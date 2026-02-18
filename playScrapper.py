from playwright.sync_api import sync_playwright
import pandas as pd

# Create an SSL context with certifi's CA bundle

url = 'https://erevuka.org/courses'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context() 
    page = context.new_page()
    
    print("Loading courses page...")
    page.goto(url, timeout=300000)
    """wait for pagination selector to appear """
    page.wait_for_selector('.pagination', timeout=130000)

    pagination = page.locator('.pagination').first

    cards = pagination.locator('.page-item')
    links = {}

    """card one is disabled and last leads nowhere so we exclude"""
    for i in range(1, cards.count()-1, 1):
        card = cards.nth(i)
        newUrl = url+f'?page={i}'
        card.click()
        """click each page to view courses {i}"""
        print(f'page {i} clicked')
        page.wait_for_selector('.row.alignment-class.mt-3', timeout = 150000)

        newRow = page.locator('.row.alignment-class.mt-3').first
        # print(newRow)

        courseCards = newRow.locator('.course-card-content')

        print('Number of course', courseCards.count())

        # page.wait_for_selector('.courses-detail-row', timeout = 180000)

        for i in range(courseCards.count()):
            href = courseCards.nth(i).locator('a').get_attribute('href')
            title = courseCards.nth(i).locator('a').get_attribute('title')
            links.update({title: {'link': href}})
        page.goto(newUrl)
    
    # Open in new page manually and close once done with scrapping
    for name in links:
        print(name)
        new_page = page.context.new_page()
        new_page.goto(links[name]['link'], wait_until="networkidle" )
        print(f'Going to page {name}')

        try:
            new_page.wait_for_selector('.row.courses-detail-row', timeout=10000)
            """Get all li of ul"""
            print('element visible')
            listItems = new_page.locator('.nav.nav-pills.course-tabs li')

            tabRefs = {}

            for k in range(0, listItems.count()-1, 1):
                first = listItems.nth(k).first
                tabTitle = first.text_content()
                tabHref = first.locator('a').get_attribute('href')
                tabRefs.update({tabTitle: links[name]['link']+tabHref })
                # print(f'clicked onn {tabTitle}')
            
            print(tabRefs)

            for ref in tabRefs:
                print(ref)
                new_page.goto(tabRefs[ref], wait_until='domcontentloaded')
                tabers = new_page.locator('ul.course-tabs a.nav-link')
                if(ref=='Description'):
                    taber = tabers.nth(0)
                    taber.click()
                    new_page.reload(wait_until='domcontentloaded')
                    new_page.wait_for_selector('.row-description',  timeout=20000)
                    child = new_page.locator('.row-description')
                    description = child.nth(0).inner_text()
                elif(ref =='Course Outline'):
                    taber = tabers.nth(1)
                    taber.click()
                    new_page.reload(wait_until='domcontentloaded')
                    new_page.wait_for_selector('.row-description',  timeout=20000)
                    child = new_page.locator('.row-description')
                    lister = child.nth(1)
                    all_texts = [li.text_content() for li in lister.locator('ul li').all()]
                    # print(all_texts, 'all textx')
                    comma_separated = ', '.join([t.strip() for t in all_texts])

                    description = comma_separated

                links[name].update({ref : description})
                    # print(links)

                # print(ref, description)
            
            

            # for k in range(0, listItems.count()-1, 1):
            #     first = listItems.nth(k).first
            #     tabTitle = first.text_content()
            #     print(f'clicked onn {tabTitle}')

                # first.click()
                # new_page.wait_for_selector('.row-description',  timeout=10000)
                # description = new_page.locator('.row-description')
                # print(description.inner_text())

            # for k in range(listItems.count()):
            #     tabTitle = listItems.nth(k).text_content()
            #     pillhref = listItems.nth(k).locator('a').get_attribute('href')

            #     tabs_page = page.context.new_page()
            #     tabs_page.goto(links[name]['link'] + pillhref)

            #     print(f'Going to page {name} +  {tabTitle}')
            #     tabs_page.wait_for_selector('.row-description',  timeout=10000)
            #     description = tabs_page.locator('.row-description')
            #     links[name].update({tabTitle : description.text_content()})
            #     print(description.text_content())
            #     tabs_page.goto(links[name]['link'])
            #     # listItems.nth(k).click(no_wait_after=True)
            #     # new_page.wait_for_selector(f'.tab-pane.active')  # Wait for tab content
            #     new_page.wait_for_timeout(300)
            #     new_page.wait_for_selector('.row-description',  timeout=10000)
            #     description = new_page.locator('.row-description')
            #     links[name].update({tabTitle : description.text_content()})
            #     print(links[name])

        except:
            print('selector not found')

        new_page.close()

    df = pd.DataFrame.from_dict(links, orient="index").reset_index().rename(columns={'index':'Course Name'})
    df.to_csv('courses-result.csv', index=False)
    # for pager in range(pagination.first.count()):
    #     card = pagination.nth(pager)
    #     print(card)
        # card.locator('.course-card-content')
        # card.click()



    # print(page)

    