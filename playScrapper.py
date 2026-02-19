from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime

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

    pages = pagination.locator('.page-item')
    links = {}
    start = datetime.now()
    """card one is disabled and last leads nowhere so we exclude"""
    for i in range(1, pages.count()-1, 1):
        pager = pages.nth(i)
        newUrl = url+f'?page={i}'
        pager.click()
        """click each page to view courses {i}"""
        print(f'page {i} clicked')
        page.wait_for_selector('.row.alignment-class.mt-3', timeout=150000)

        newRow = page.locator('.row.alignment-class.mt-3').first
        # print(newRow)

        courseCards = newRow.locator('.course-card-content')

        cardFooters = newRow.locator('.card-footer')

        print(f'Number of courses on page {i}', courseCards.count())

        for i in range(courseCards.count()):
            href = courseCards.nth(i).locator('a').get_attribute('href')
            title = courseCards.nth(i).locator('a').get_attribute('title')
            """fetching the second child of the footer"""
            action = cardFooters.nth(i).locator('a')
            lastAction = action.last
            """We check if the action text is all modules extract inner modules links"""
            if (lastAction.text_content() == 'All Modules'):
                innerPage = page.context.new_page()
                innerPage.goto(lastAction.get_attribute(
                    'href'), wait_until='domcontentloaded')
                print(f'Opening inner pages for {title}')
                innerPage.wait_for_selector(
                    '.row.alignment-class.mt-3', timeout=150000)
                innerRow = innerPage.locator('.row.alignment-class.mt-3').last
                """There are rows in the inner page so we pick the last one"""
                innerCards = innerRow.locator('.course-card-content')
                print('Extracting links for inner pages')
                for j in range(innerCards.count()):
                    innerHref = innerCards.nth(j).locator(
                        'a').get_attribute('href')
                    innerTitle = innerCards.nth(j).locator('a').inner_text()
                    links.update({innerTitle: {'link': innerHref}})
                innerPage.close()
            else:
                links.update({title: {'link': href}})

        page.goto(newUrl)

    print(f'Done extracting links. Total links extracted: {len(links)}')
    print('Scrapping of each page')
    """Open in new page manually and close once done with scrapping"""
    for name in links:
        new_page = page.context.new_page()
        new_page.goto(links[name]['link'], wait_until="networkidle")
        # print(f'Extracting description and outlines of {name} course')
        try:
            new_page.wait_for_selector(
                '.row.courses-detail-row', timeout=10000)
            # print('Details row visible proceed')

            """Get all the tabs on the details page we will exclude testimonials.
            Since the tabs reload the dom we extract their hrefs for each course
            """

            listItems = new_page.locator('.nav.nav-pills.course-tabs li')

            tabRefs = {}

            for k in range(0, listItems.count()-1, 1):
                first = listItems.nth(k).first
                tabTitle = first.text_content()
                tabHref = first.locator('a').get_attribute('href')
                tabRefs.update({tabTitle: links[name]['link']+tabHref})
                # print(f'clicked onn {tabTitle}')
            """For each tab click and wait to load to extract content before proceeding.
            The clicks are fast so we have reload the page for second tab click.
            """
            for ref in tabRefs:
                new_page.goto(tabRefs[ref], wait_until='domcontentloaded')
                tabers = new_page.locator('ul.course-tabs a.nav-link')
                if (ref == 'Description'):
                    taber = tabers.nth(0)
                    taber.click()
                    new_page.wait_for_selector(
                        '.row-description',  timeout=20000)
                    child = new_page.locator('.row-description p')
                    description = child.nth(0).inner_text()
                elif (ref == 'Course Outline'):
                    taber = tabers.nth(1)
                    taber.click()
                    new_page.reload(wait_until='domcontentloaded')
                    new_page.wait_for_selector(
                        '.row-description',  timeout=20000)
                    child = new_page.locator('.row-description')
                    lister = child.nth(1)
                    """extract li items to comma separated string"""
                    all_texts = [li.text_content()
                                for li in lister.locator('ul li').all()]
                    comma_separated = ', '.join([t.strip() for t in all_texts])

                    description = comma_separated

                links[name].update({ref: description})
            # print(f'Course description and outline updated.')

        except:
            print('Course details selector not found')

        new_page.close()
    df = pd.DataFrame.from_dict(links, orient="index").reset_index().rename(
        columns={'index': 'Course Name'})
    df.to_csv('./datasets/courses-result.csv', index=False)
    records = df.shape[0]
    end = datetime.now()    
    print('Task ended on ', end)
    print('process took', end - start)
    print(f'Task Completed. {records} Record Saved!!')
