from playwright.sync_api import Playwright, sync_playwright

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    # Recommended: set a standard viewport and longer default timeout for slow gov servers
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.set_default_timeout(60000)

    try:
        # 1. Navigate directly to the starting page
        page.goto("https://webgis2.mpbhulekh.gov.in/#/home", wait_until="networkidle")

        # 2. Open dashboard navigation
        page.get_by_role("button", name="Dashboard & Reporting").click()
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="आदेश अनुपालन").click()
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="आदेश अनुपालन निगरानी").click()
        page.wait_for_timeout(3000)
        # 3. Reference the report iframe directly
        report_frame = page.frame_locator('iframe[title="Report"]')

        # Wait for the report container inside the iframe to appear
        report_frame.locator("vr-multiheadertable-preview").first.wait_for(state="visible", timeout=60000)

        # 4. District selection and row drill-downs
        district_select = report_frame.locator("vr-multiheadertable-preview").filter(
            has_text="Created with Sketch. जिला ▲▼नामांतरण एवं बटवारा (RCMS"
        ).get_by_role("combobox")
        district_select.wait_for(state="visible")
        district_select.select_option("50")

        # Wait briefly for AJAX refresh before clicking rows
        page.wait_for_timeout(2000)
        report_frame.get_by_role("cell", name="जबलपुर").first.click()

        page.wait_for_timeout(2000)
        report_frame.get_by_role("cell", name="जबलपुर").nth(1).click()

        # 5. Open export menu
        svg_btn = report_frame.locator("vr-multiheadertable-preview").filter(
            has_text="Created with Sketch. ग्राम ▲▼"
        ).get_by_label("Inline Svg")
        svg_btn.wait_for(state="visible")
        svg_btn.click()

        # 6. Synchronous Download Handling (Fixes premature closing)
        xls_btn = report_frame.get_by_role("menuitem", name="XLS")
        xls_btn.wait_for(state="visible")

        print("Waiting for download to trigger...")
        with page.expect_download(timeout=120000) as download_info:
            xls_btn.click()

        download = download_info.value
        save_path = "./adesh_anup.xls"
        download.save_as(save_path)
        print(f"Download successfully saved to: {save_path}")

    except Exception as e:
        print(f"Execution Error: {e}")
    finally:
        context.close()
        browser.close()

if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)