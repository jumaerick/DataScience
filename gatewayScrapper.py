from playwright.sync_api import sync_playwright

url = 'https://dev.financinggateway.org/resources'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    print('loading page')
    page.goto(url, timeout=300000)
    try:
        page.wait_for_selector('.hamburgerMenu', timeout= 3000)
        hMenu = page.locator('.hamburgerMenu')
        print('found menu item')
        menu = hMenu.first
        print('clicked on menu item')
        menu.click()
        page.wait_for_selector('#menuModal', timeout= 30000)
        menuModal = page.locator('#menuModal')
        menuItem = menuModal.locator('.menuItems')
        lis = menuItem.locator('a:not([href="#"])')
        # lis = menuItem.locator('ul li:not(.dropdown)')
        # menuList = menu.locator('ul li').all()
        # menuList = menuItem.locator('ul li')
        instruments = ['Find Financing Options']
        links = {}
        for i in range(lis.count()):
            if (lis.nth(i).text_content() in instruments):
                links.update({lis.nth(i).text_content(): lis.nth(i).get_attribute('href')})
        print('links to extract')
        print(links)
        subLink = page.context.new_page()
        for new in links:
            prods = {}
            print(f'going to {links[new]}')
            subLink.goto(links[new], timeout=300000)
            table = subLink.locator('#resultsTable')
            counter = subLink.locator('.results-count').text_content()
            ths = table.locator('th')
            trs = table.locator('.facilityRow')
            # print(counter)
            print(trs.count())
            for i in range(ths.count()):
                th = ths.nth(i)
                title = ths.nth(i).text_content()
                if(ths.nth(i).locator('a').count() > 0):
                    title = title.replace('Sort', '')
                prods.update({title:[]})

            for j in range(trs.count()):
                tds = trs.nth(j).locator('td').all()
                print(tds)
                # for td in range(tds.count()):
                #     print(td.nth(text_content())

            print(prods)
        subLink.close()

    except:
        print('no menu item found')
    print('done')