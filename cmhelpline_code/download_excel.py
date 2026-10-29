from playwright.sync_api import sync_playwright
import os
#L-1 complain download function
os.makedirs('cmhelpline', exist_ok=True)
import os

def download_file(page, locator, save_path):
    print(f"Starting download for {save_path}...")
    
    # Clean up the old file if it exists
    if os.path.exists(save_path):
        os.remove(save_path)
        
    # Block execution until the specific download triggered by the click is captured
    with page.expect_download() as download_info:
        page.wait_for_selector(locator).click()
        
    # Save the captured download to your dynamic path
    download = download_info.value
    download.save_as(save_path)
    print(f"Download completed: {save_path}")