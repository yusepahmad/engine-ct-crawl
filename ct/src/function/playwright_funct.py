import asyncio

class ControllerAutomation():
    async def crawl_url(self, url):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            page.goto(url)
            print(page.inner_text('//*[@id="block-ctdc-system-main"]/div/div/div[2]/div/div/div/article/div/div[2]/div'))

            print(page)

            await page.close()