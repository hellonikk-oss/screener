from playwright.sync_api import sync_playwright
import os
import shutil

os.makedirs('./cmhelpline', exist_ok=True)

def download_handle(download):
    print('download started')
    for f in ['./cmhelpline/swamitv.xls', './cmhelpline/swamitv.xlsx']:
        if os.path.exists(f):
            os.remove(f)
  
    download.save_as('./cmhelpline/swamitv.xlsx')
    shutil.copyfile('./cmhelpline/swamitv.xlsx', './cmhelpline/swamitv.xls')
    print('download completed')
    

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://services.mpigr.gov.in/svamitva_dashboard/')
    print('open')
    page.wait_for_selector("//a[contains(text(),'जबलपुर')]").click()
    page.wait_for_selector("//a[contains(text(),'जबलपुर')]").click()
    page.on('download', download_handle) 
    page.wait_for_selector("//button[contains(text(),'⬇ Download Excel')]").click()
    page.wait_for_timeout(5000)
    browser.close()
