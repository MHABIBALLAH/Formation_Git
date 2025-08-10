import asyncio
import time
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Generate a unique username for this test run
        unique_username = f"testuser_{int(time.time())}"
        password = "password123"

        # 1. Navigate to the app
        await page.goto("http://127.0.0.1:5000")

        # 2. Wait for the initial auth check to complete (loading view to disappear)
        await expect(page.locator("#loading-view")).to_be_hidden(timeout=10000)

        # 3. Now, the auth view with the login form should be visible
        await expect(page.locator("#auth-view")).to_be_visible()
        await expect(page.locator("#login-form-container")).to_be_visible()
        await expect(page.locator("h2").get_by_text("Connexion")).to_be_visible()

        # 3. Switch to registration form
        await page.locator("#show-register-link").click()
        await expect(page.locator("#register-form-container")).to_be_visible()

        # 4. Fill and submit registration form
        await page.locator("#register-username").fill(unique_username)
        await page.locator("#register-password").fill(password)
        await page.locator("#register-form button").click()

        # 5. Wait for success message and automatic switch to login
        await expect(page.locator("#register-message")).to_have_text("Inscription réussie ! Vous pouvez maintenant vous connecter.")
        await expect(page.locator("#login-form-container")).to_be_visible(timeout=5000)

        # 6. Fill and submit login form
        await page.locator("#login-username").fill(unique_username)
        await page.locator("#login-password").fill(password)
        await page.locator("#login-form button").click()

        # 7. Wait for dashboard to be visible
        await expect(page.locator("#dashboard-view")).to_be_visible(timeout=10000)

        # 8. Assert a key element is present and data has loaded
        summary_title = page.locator("h2.page-title").get_by_text("Résumé Financier")
        await expect(summary_title).to_be_visible()
        total_revenue_element = page.locator("#total-revenue")
        # Wait for the fetch to complete by checking that the value is not the default '--'
        await expect(total_revenue_element).not_to_have_text("--", timeout=10000)

        # 9. Take a screenshot
        await page.screenshot(path="jules-scratch/verification/auth_flow_success.png")

        print("Playwright script completed successfully and took a screenshot.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
