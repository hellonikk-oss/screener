from playwright.sync_api import sync_playwright
import os

from requests import delete
state_file = 'state_CM.json'
if os.path.exists(state_file):
    os.remove(state_file)
    
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    try:
        print("Opening login page...")
        page.goto('https://cmhelpline.mp.gov.in/MIS/Default.aspx', timeout=30000)
        page.wait_for_load_state('networkidle')
        print("Login page opened.")

        # Enter username
        username = page.wait_for_selector('//input[@id="txtUser"]', timeout=10000)
        username.fill('REV_TAH_BARE_JAB')
        print("Username entered.")

        # Enter password
        password = page.wait_for_selector('//input[@id="txtPass"]', timeout=10000)
        password.fill('71671')
        print("Password entered.")

        # Wait for CAPTCHA input
        print("Please enter the CAPTCHA displayed on the screen.")
        captcha_input = input("Enter CAPTCHA: ")
        captcha_field = page.wait_for_selector('//input[@id="txtCaptcha"]', timeout=10000)
        captcha_field.fill(captcha_input)
        print("CAPTCHA entered.")

        # Click submit button
        try:
            button = page.wait_for_selector("//input[@id='btnsubmit']", timeout=10000)
            button.click()
            print("Login button clicked.")
        except Exception as e:
            print("Login button not found. Error:", e)
            raise

        # Wait for successful login
        page.wait_for_load_state('networkidle', timeout=15000)
        print("Login successful.")

        # Save session state
        context.storage_state(path='state_CM.json')
        print("Session state saved to state.json.")

    except Exception as e:
        print("An error occurred:", e)
        page.screenshot(path='error_screenshot.png')
        print("Screenshot saved as error_screenshot.png for debugging.")

    finally:
        browser.close()