import asyncio
from dotenv import load_dotenv
import os

from scrapybara import Scrapybara
from undetected_playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

load_dotenv()
api_key = os.getenv('API_KEY')

async def get_scrapybara_browser():
    client = Scrapybara(api_key=api_key)
    instance = client.start_browser()
    return instance

def check_visited(checked, text_contents):
    if(len(text_contents) == 0):
        return False
    for name in checked:
        if name in text_contents[0]:
            return True
    return False

async def retrieve_menu_items(instance, start_url: str) -> list[dict]:
    """
    :args:
    instance: the scrapybara instance to use
    url: the initial url to navigate to

    :desc:
    this function navigates to {url}. then, it will collect the detailed
    data for each menu item in the store and return it.

    (hint: click a menu item, open dev tools -> network tab -> filter for
            "https://www.doordash.com/graphql/itemPage?operation=itemPage")

    one way to do this is to scroll through the page and click on each menu
    item.

    determine the most efficient way to collect this data.

    :returns:
    a list of menu items on the page, represented as dictionaries
    """
    cdp_url = instance.get_cdp_url().cdp_url
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(cdp_url)
        page = await browser.new_page()
        await page.goto(start_url)

        address_input_locator = page.get_by_test_id("AddressAutocompleteField")
        try:
            await address_input_locator.fill('University of Waterloo')
            await address_input_locator.click()
            await page.keyboard.press('Enter')   
            await page.locator("[aria-label*='Close']").click()
        except PlaywrightTimeoutError:
            pass

        previous_scroll = 0
        menu_item_locator = page.get_by_test_id("MenuItem")
        result = []
        visited = set()

        while True:
            try:
                await page.wait_for_load_state('networkidle')
                menu_items = await menu_item_locator.all()
                print(await menu_item_locator.count())
                for menu_item in menu_items:
                    item_id = await menu_item.get_attribute("data-item-id")
                    if item_id not in visited:
                        async with page.expect_response("https://www.doordash.com/graphql/itemPage?operation=itemPage") as response_info:
                            await menu_item.click()
                            await page.locator("[aria-label*='Close']").click()
                        response = await response_info.value
                        data = await response.json()
                        print(item_id)
                        name = data['data']['itemPage']['itemHeader']['name']
                        print(name)
                        result.append(data)
                        visited.add(item_id)
            except PlaywrightTimeoutError:
                pass
            finally:
                current_scroll = previous_scroll + await page.evaluate("window.innerHeight")
                await page.evaluate(f"() => window.scroll(0, {current_scroll})")
                current_scroll = await page.evaluate("window.scrollY")

                print(previous_scroll)
                print(current_scroll)

                if(previous_scroll == current_scroll):
                    break

                previous_scroll = current_scroll


async def main():
    instance = await get_scrapybara_browser()

    try:
        await retrieve_menu_items(
            instance,
            "https://www.doordash.com/store/panda-express-san-francisco-980938/12722988/?event_type=autocomplete&pickup=false",
        )
    finally:
        # Be sure to close the browser instance after you're done!
        instance.stop()


if __name__ == "__main__":
    asyncio.run(main())