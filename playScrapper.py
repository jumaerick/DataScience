from playwright.sync_api import sync_playwright


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

    """card one is disabled and last leads nowhere so we exclude"""
    for i in range(1, cards.count() - 1, 1):
        card = cards.nth(i)
        url = url+f'?page={i}'
        card.click()
        """click each page to view courses {i}"""
        print(f'page {i} clicked')
        page.wait_for_selector('.row.alignment-class.mt-3', timeout = 150000)

        newRow = page.locator('.row.alignment-class.mt-3').first
        # print(newRow)

        courseCards = newRow.locator('.course-card-content')

        print('Number of course', courseCards.count())

        # page.wait_for_selector('.courses-detail-row', timeout = 180000)

        for k in range(courseCards.count()):
            courseCard = courseCards.nth(k).first
            courseCard.click()
            print(f'Clicked course card {k}')
            # page.wait_for_selector('.courses-detail-row', timeout = 180000)
            # page.wait_for_load_state("networkidle")
            # detailsRow = page.locator('.courses-detail-row')
            # if detailsRow.count() > 0:
            
            #     tabs = page.locator('.nav-item')
            #     print(tabs.count())
                # print('tabs', detailsRow.first.inner_text())

                # """Excluding the testionials tab"""
                # for j in range(0, tabs.count()-1, 1):
                #     tab = tabs.nth(j)
                #     """Clicking tab"""
                #     tab.click()
                #     print(f"tab {tab.inner_text()} clicked")
            page.goto(url)
        # break

    # for pager in range(pagination.first.count()):
    #     card = pagination.nth(pager)
    #     print(card)
        # card.locator('.course-card-content')
        # card.click()



    # print(page)

    