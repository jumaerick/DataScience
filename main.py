from playwright.sync_api import sync_playwright
import pandas as pd

url = "https://ecatalogue.firabarcelona.com/barcelonawineweek2026/home?filter=ONLY_EXHIBITORS&lang=en_GB"

def dismiss_cookie_banner(page):
    try:
        banner = page.locator("#usercentrics-cmp-ui")
        # Direct check for the button inside shadow DOM or standard DOM
        accept_btn = page.get_by_role("button", name="Accept all")
        if accept_btn.count() > 0:
            accept_btn.click()
            page.wait_for_timeout(1000)
    except:
        pass

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context() 
    page = context.new_page()
    
    print("Loading landing page...")
    page.goto(url, wait_until="networkidle")
    dismiss_cookie_banner(page)

    # --- STEP 1: EXPANSION ---
    print('Starting list expansion...')
    max_batches = 15 # Set this higher (e.g., 150) to get all 1,354 items
    batch = 0
    while batch < max_batches:
        see_more = page.locator('.see_more_button:visible')
        if see_more.count() > 0:
            see_more.first.click()
            batch += 1
            # Wait for items to actually load
            page.wait_for_timeout(2000) 
            if batch % 5 == 0: print(f"Expanded {batch} batches...")
        else:
            break

    # --- STEP 2: COLLECTION ---
    cards_titles = page.locator("div.ex.ex--list .ex__data-title")
    company_names = [cards_titles.nth(i).get_attribute("title") for i in range(cards_titles.count())]
    print(f"Collected {len(company_names)} names. Starting deep scrape...")

    # --- STEP 3: SEARCH-AND-SCRAPE ---
    companyDic = {}
    
    for i, name in enumerate(company_names):
        print(f"[{i+1}/{len(company_names)}] Scraping: {name}")
        
        try:
            # 1. Clear and fill search safely
            search_input = page.locator("input.search_input").first
            search_input.click(click_count=3) # Highlight existing text
            page.keyboard.press("Backspace")
            search_input.fill(name)
            page.keyboard.press("Enter")
            
            # 2. Wait for result to filter
            page.wait_for_selector("div.ex.ex--list", timeout=15000)
            page.locator("div.ex.ex--list").first.click()

            # 3. Wait for Detail Page to fully load
            page.wait_for_load_state("networkidle")
            page.wait_for_selector(".detail-content__title", timeout=20000)

            # --- DATA EXTRACTION ---
            company_title = page.locator(".detail-content__title").inner_text()
            
            # Initialize storage for this company
            company_info = {
                'Description': page.locator('.detail-content__description').inner_text() if page.locator('.detail-content__description').count() > 0 else "",
                'Trade Show Location': page.locator('.detail-map__location').inner_text() if page.locator('.detail-map__location').count() > 0 else "",
                'Website': '', 'Phone': '', 'Location': ''
            }

            # Contacts
            contacts = page.locator('.detail-contact__item')
            for w in range(contacts.count()):
                item = contacts.nth(w)
                text = item.inner_text().strip()
                if not text: continue
                
                if item.locator('.is-link').count() > 0:
                    company_info['Website'] = text
                elif text.startswith('+') or any(char.isdigit() for char in text[:3]):
                    company_info['Phone'] = text
                else:
                    company_info['Location'] = text

            # Products
            product_cards = page.locator('.ex.ex--list') # The cards inside the detail page
            for k in range(product_cards.count()):
                p_title = product_cards.nth(k).locator(".ex__data-title").inner_text()
                company_info[f"Product {k+1}"] = p_title

            companyDic[company_title] = company_info

            # 4. RESET STATE - Go back to search
            page.go_back()
            page.wait_for_selector("input.search_input", timeout=10000)

        except Exception as e:
            print(f"Server lag or Error for {name}. Resetting... ({e})")
            page.goto(url, wait_until="networkidle")
            dismiss_cookie_banner(page)

    # Export
    df = pd.DataFrame.from_dict(companyDic, orient="index").reset_index().rename(columns={'index':'Winery Name'})
    df.to_csv('firabarcelona_results.csv', index=False)
    print("Done! File saved.")