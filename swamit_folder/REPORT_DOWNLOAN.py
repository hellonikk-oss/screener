from playwright.sync_api import sync_playwright
import os
import sys

# Ensure UTF-8 output encoding for Windows terminal
sys.stdout.reconfigure(encoding='utf-8')

# L-1 complain download function
os.makedirs('file', exist_ok=True)

def download_handle_district(download):
    print('download started')
    if os.path.exists('./file/district.xls'):
        if os.path.exists('./file/district_old.xls'):
            os.remove('./file/district_old.xls')
        os.rename('./file/district.xls', './file/district_old.xls')
    download.save_as('./file/district.xls')  # provide the path where you want to save the downloaded file
    print('download completed District')

def download_handle_block(download):
    print('download started')
    if os.path.exists('./file/block.xls'):
        if os.path.exists('./file/block_old.xls'):
            os.remove('./file/block_old.xls')
        os.rename('./file/block.xls', './file/block_old.xls')
    download.save_as('./file/block.xls')  # provide the path where you want to save the downloaded file
    print('download completed Block')
    
    
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
      
    page.goto('https://services.mpigr.gov.in/svamitva_dashboard/', timeout=30000)
    page.wait_for_load_state('networkidle', timeout=15000)
     
    try:
        # 1. Download District level report
        excel_download = page.wait_for_selector("#viewDownloadBtn", timeout=10000)
        with page.expect_download() as download_info:
            excel_download.click(force=True)  # Force the click even if Playwright thinks it is hidden
        download = download_info.value
        download_handle_district(download)
        page.wait_for_load_state('networkidle', timeout=15000)
        
        # table = page.locator("//table[@id='districtTable']", timeout=10000)
        # rows = table.locator("tr")
        # district_row= rows.nth(15).locator("td")
               
        # 2. Click district row to open block-level view
        page.wait_for_selector("//a[contains(text(),'जबलपुर')]").click()
        # district_link = page.wait_for_selector("(//td[@class='cell-sno' and text()='1']/following-sibling::td[@class='cell-wrap'])[1]", timeout=10000)
        # district_link.click(force=True)
        page.wait_for_load_state('networkidle', timeout=15000)

        # 3. Download Block level report
        block_download = page.wait_for_selector("button.btn-download-excel", timeout=30000)
        with page.expect_download() as download_info:
            block_download.click(force=True)
        download = download_info.value
        download_handle_block(download)
                           
    except Exception as inner_e:
        print(f"\n[X] Error during execution: {inner_e}")
        
    except Exception as e:
        print(f"\n[X] Error: {e}")
        print("\nPossible reasons:\n website server error, network connectivity issue, or the element not being found.")
    
    finally:
        browser.close()
