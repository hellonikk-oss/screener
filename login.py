from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser=p.chromium.launch(headless=False)
    context=browser.new_context()
    context = browser.new_context(storage_state="state.json")
    page = context.new_page()
    page.goto('https://www.screener.in/company/TVSMOTOR/consolidated/')
    page.wait_for_timeout(10000)
    print ('successfully login  ')
   
    browser.close()