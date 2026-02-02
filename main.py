from playwright.sync_api import sync_playwright
import math
import pandas as pd
from playwright.sync_api import TimeoutError

url = "https://ecatalogue.firabarcelona.com/barcelonawineweek2026/home?filter=ONLY_EXHIBITORS&lang=en_GB"

data = {}

def dismiss_cookie_banner(page):
    # locate the banner
    banner = page.locator("#usercentrics-cmp-ui")
    if banner.count() > 0:
        # click the "Accept all" button
        accept_btn = banner.locator("button:has-text('Accept all')")
        if accept_btn.count() > 0:
            accept_btn.first.click()
            page.wait_for_timeout(500)  # short pause to let it disappear


def get_optional_text(page, selector, timeout=3000):
    el = page.locator(selector)
    try:
        el.wait_for(state="visible", timeout=timeout)
        return el
    except TimeoutError:
        return None


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(url, wait_until="networkidle")

    # Wait for the main content container (replace selector with the real one)
    page.wait_for_selector("app-home >> *", timeout=60000)

    # Now grab the text or HTML you need
    content = page.content()
    # Example: get all exhibitor names
    # exhibitors = page.locator(".ex-img").first.get_attribute('src')
    # titles = page.locator(".detail-contact__item .is-link").first
    # print(titles)
    # cards = page.locator("div.ex.ex--list")
    # cards = page.locator("div.ex.ex--list")
    # count = cards.count()

    # for i in range(count):
    #     card = cards.nth(i)
        
    #     name = card.locator(".ex__data-title").inner_text()
    #     img = card.locator("img.ex-img").get_attribute("src")
    #     desc = card.locator(".description").first.inner_text()
    #     stand = card.locator("app-stand-display").inner_text()

    #     print(name, img, desc, stand)
    dismiss_cookie_banner(page)

    totalItems = page.locator('.counter')

    itemsCount = 0
    batch = 0

    if(totalItems.count() > 0):
        itemsCount = int(totalItems.first.inner_text().split(' ')[0])
        batch = math.ceil(itemsCount//9)
    # print(itemsCount)

    # i = 1
    # while i<2:
    #     seeMoreButton = page.locator('.see_more_button')
    #     if (seeMoreButton.count() > 0):
    #         seeMoreButton.first.click()
    #         page.wait_for_timeout(3000)
    #     i+=1
    dismiss_cookie_banner(page)
    total = 0
    itemsDic = dict()
    # Start expanding the list
    print("Expansion started...")
    t = 0
    while True:
        # 1. Look for the button specifically if it's visible
        see_more = page.locator('.see_more_button:visible')
        
        # 2. If it exists, click it
        if ((see_more.count() > 0) & (t!=0)):
            # Capture how many items we have BEFORE clicking
            current_count = page.locator("div.ex.ex--list").count()
            t+=1
            print(f"Items found so far: {current_count}. Clicking 'See More'...")
            see_more.first.click()
            # t+=1
            
            # 3. Wait for the items to actually load (the count should increase)
            try:
                page.wait_for_function(
                    f"document.querySelectorAll('div.ex.ex--list').length > {current_count}",
                    timeout=10000
                )
                # Optional: a tiny pause to let the UI settle
                page.wait_for_timeout(1000) 
            except:
                print("Timed out waiting for new items. Proceeding with what we have.")
                break
        else:
            # 4. If the button is gone, we are finished expanding!
            print("No more 'See More' button found. List is fully expanded.")
            break

    page.wait_for_selector("div.ex.ex--list", timeout=20000)
    cards = page.locator("div.ex.ex--list")
    count = cards.count()
    print(count)

    # for i in range(count):
    #     card = cards.nth(i)
    #     name = card.locator(".ex__data-title")
    #     if name.count()>0:
    #         print(f'opening up {name.inner_text()}')
    #         itemsDic.update({name.inner_text(): name.count()})

    page.wait_for_selector("div.search_bar1", timeout=20000)
    df_names = pd.read_csv('product_names.csv')
    searchNames = df_names.iloc[:, 0].values[:3]
    print(searchNames)
    search = page.locator('.search_input:visible')
    dismiss_cookie_banner(page)
    companyDic = {}
    
    if search.count() > 0:
        for searchTerms in searchNames:
            search.first.click()
            search.first.fill('')  # clear just in case
            search.first.type(searchTerms)
            try:
                page.wait_for_selector('.counter', timeout=5000)
                results = page.locator('.counter')
                # print(results.count(), 'hapa')
                searchItems = results.count()
                if searchItems > 0:
                    page.wait_for_selector("div.ex.ex--list", timeout=30000)
                    cards = page.locator("div.ex.ex--list")
                    count = cards.count()

                if count > 0:
                    for j in range(count):
                        card = cards.nth(j)
                        name = card.locator(".ex__data-title")
                        # print('na hapa')
                        if name.count()>0:
                            if(name.inner_text() == searchTerms ):
                                print(f'opening child up {name.inner_text()}')

                                card.scroll_into_view_if_needed()
                                card.click() 
                                # wait for products container (update selector as needed)
                                page.wait_for_selector(".detail--exhibitor", timeout=20000)
                                page.wait_for_selector(
                                    ".detail-content__title",
                                    state="attached",
                                    timeout=20000
                                )

                                # page.wait_for_selector(
                                #     ".ex__data",
                                #     state="attached",
                                #     timeout=5000
                                # )

                                products = page.locator('.ex__data')

                                # wait a short time for the first product to appear
                                try:
                                    products.first.wait_for(state="attached", timeout=3000)  # 3 seconds
                                except TimeoutError:
                                    # element didn't appear — no products
                                    products_count = 0
                                else:
                                    products_count = products.count()
                                # print(products_count)

                                productNames = page.locator('.product__exhibitor-name')

                                company = page.locator(".detail-content__title").inner_text()

                                #Handling missing information
                                company_description = ''
                                product_titles, product_descriptions = [], []
                                website, phone, address,social = '','','', ''

                                if(page.locator('.detail-content__description').count() > 0):
                                    company_description = page.locator('.detail-content__description').inner_text()

                                trade_show_location = page.locator('.detail-map__location').inner_text()
                                # print(company_description)

                                for j in range(products_count):
                                    title_locator = products.nth(j).locator(".ex__data-title")
                                    if title_locator.count() > 0:
                                        product_titles.append(title_locator.inner_text())
                                    else:
                                        product_titles.append(None) 
                                # if(products.count() > 0):
                                #     product_titles = [products.nth(j).locator(".ex__data-title").inner_text() for j in range(products.count())]
                                product_descriptions = [productNames.nth(j).inner_text() for j in range(productNames.count())]
                                contacts = page.locator('.detail-contact__item')
                                

                                for w in range(contacts.count()):
                                    contact = contacts.nth(w)
                            
                                    if(len(contact.inner_text()) > 0):
                                        if (contact.locator('.is-link').count()>0):
                                            website= contact.inner_text()
                                            # print('website')
                                        elif(contact.locator('.social-links').count() > 0):
                                            social = contact.inner_text()
                                            # print('social')
                                        elif( contact.inner_text()[0] == '+'):
                                            phone = contact.inner_text()
                                            # print('phone')
                                        else:
                                            address = contact.inner_text()
                                            # print('address')
                                    else:
                                        pass

                                companyDic.update({company: {'Winery Description': company_description,'Website': website, 
                                                            'Winery Location': address, 'Phone #': phone, 'Trade Show Location':trade_show_location}})
                                
                                for k in range(len(product_titles)):
                                    companyDic[company][f"Product {k+1} Name"] = product_titles[k]
                                    companyDic[company][f"Product {k+1} Description"] = product_descriptions[k]

                                # print("Products:", product_descriptions)
                                # print(product_titles)
                                # print(page.locator('.product__exhibitor-name').count())
                                page.go_back()
                                page.wait_for_load_state("domcontentloaded")
                                # print(items)

                                page.wait_for_selector("div.ex.ex--list", timeout=20000)
                            else:
                                pass
            except:
                continue
                print('could not find the results')
            page.wait_for_timeout(60000)


    df = pd.DataFrame.from_dict(companyDic, orient="index").reset_index()
    # df_products = pd.DataFrame.from_dict(productDic, orient="index").reset_index()
    df.rename(columns={'index':'Winery Name'}, inplace=True)
    df.to_csv('test.csv',index=None)


