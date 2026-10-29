from playwright.sync_api import sync_playwright
import os
from download_excel import download_file  # Import the reusable function

# Create the directory
os.makedirs('cmhelpline', exist_ok=True)

# Reusable helper function for downloading files dynamically
def download_file(page, locator, save_path):
    print(f"Starting download for {save_path}...")
    
    if os.path.exists(save_path):
        os.remove(save_path)
        
    with page.expect_download(timeout=60000) as download_info:
        page.wait_for_selector(locator).click()
        
    download = download_info.value
    download.save_as(save_path)
    print(f"Download completed: {save_path}")


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    
    # Check if state.json exists
    if not os.path.exists("state_CM.json"):
        print("Error: state.json not found!")
        print("Please run storage_state_cmhelpline.py first to create the session")
        browser.close()
        exit()
    
    try:
        print("=" * 60)
        print("LOADING SAVED SESSION FROM state.json")
        print("=" * 60)
        
        # Use saved session with custom User-Agent
        print("\n1. Creating context with saved session and custom User-Agent...")
        context = browser.new_context(
            storage_state="state_CM.json",
            #user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        print("   ✓ Session loaded with custom User-Agent")
        
        # Navigate to dashboard
        print("\n2. Opening dashboard...")
        page.goto('https://cmhelpline.mp.gov.in/MIS/dashboard.aspx', timeout=30000)
        page.wait_for_load_state('networkidle', timeout=15000)
        print("   ✓ Dashboard opened successfully")
        
        try:
            # Wait for the element to be attached to the DOM (ignoring visibility)
            L1 = page.wait_for_selector("//a[@id='WIPLink']", state="attached", timeout=10000)

            # Force the click even if Playwright thinks it is hidden
            L1.click(force=True)
            
            all_complain = page.wait_for_selector("//a[contains(@href,'complaintlist.aspx?type=1')]", timeout=5000)
            all_complain.click()
            
            # Use the reusable function to trigger and save the download
            download_file(
                page=page,
                locator='input#ctl00_ContentPlaceHolder1_btnExelExport',
                save_path='./cmhelpline/cmhelpline_1.xls'
            )
            
            # Safely navigate back to dashboard now that the download is definitely complete
            page.goto('https://cmhelpline.mp.gov.in/MIS/dashboard.aspx', timeout=30000)   
            page.wait_for_load_state('networkidle', timeout=15000)

            # Click on 'उच्च लेवल पर लंबित शिकायतें' to view L2, L3, L4 table
            box = page.wait_for_selector("//div[contains(@class, 'cm-box-green') and .//span[text()='उच्च लेवल पर लंबित शिकायतें']]", timeout=10000)
            box.click()
            page.wait_for_load_state('networkidle', timeout=15000)

            levels = [
                ('L2', 2, './cmhelpline/cmhelpline_L2.xls'),
                ('L3', 3, './cmhelpline/cmhelpline_L3.xls'),
                ('L4', 4, './cmhelpline/cmhelpline_L4.xls')
            ]

            for name, col_idx, save_path in levels:
                print(f"\n--- Downloading {name} ---")
                if "TimeLimitExceededcomplaints.aspx" not in page.url or "TimeLimitExceededcomplaints_AttriWise.aspx" in page.url:
                    page.goto('https://cmhelpline.mp.gov.in/MIS/TimeLimitExceededcomplaints.aspx', timeout=30000)
                    page.wait_for_load_state('networkidle', timeout=15000)

                td_link = page.wait_for_selector(
                    f"//table[contains(@class, 'cm-margin-top-60') and contains(@class, 'table-hover')]//tr[1]//td[{col_idx}]//a",
                    timeout=10000
                )
                td_link.click()
                page.wait_for_load_state('networkidle', timeout=15000)

                download_file(
                    page=page,
                    locator='input#ctl00_ContentPlaceHolder1_btnExelExport',
                    save_path=save_path
                )      
        except Exception as inner_e:
            print(f"\n✗ Error during error handling: {inner_e}")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nPossible reasons:")
        print("1. Session expired - run storage_state_cmhelpline.py again")
        print("2. Website server error")
        print("3. Network connectivity issue")
        
    finally:
        browser.close()