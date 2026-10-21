from playwright.sync_api import sync_playwright
import os
#L-1 complain download function
os.makedirs('cmhelpline', exist_ok=True)
def download_handle(download):
    print('download started')
    if os.path.exists('./cmhelpline/cmhelpline_1.xls'):
        os.remove('./cmhelpline/cmhelpline_1.xls')
  
    download.save_as('./cmhelpline/cmhelpline_1.xls')  # provide the path where you want to save the downloaded file
    print('download completed')
    
    
    
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
            all_complain=page.wait_for_selector("//a[contains(@href,'complaintlist.aspx?type=1')]", timeout=5000)
            all_complain.click()
            page.on('download', download_handle)   
            page.wait_for_selector('input#ctl00_ContentPlaceHolder1_btnExelExport').click()
                            
                    
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