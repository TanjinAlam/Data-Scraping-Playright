import asyncio
import csv
from datetime import datetime
from playwright.async_api import async_playwright

class PlayWrightScraper:
    @staticmethod
    async def search(search_url: str):
        result = "No"  # Default result
        
        base_url = "https://www.yellowpages.net/places"
        async with async_playwright() as p:
            for browser_type in [p.chromium]:
                browser = await browser_type.launch(headless=True)
                
                #External Proxy 
                # try:
                #     # browser = await browser.new_context(proxy={"server": "http://proxy.proxyverse.io:9200:country-nl-session-2d1601940904441a90c9fc9fdc64fd3a:2081b12e-8718-46c7-a088-45e19ec182c4"})
                #     pass
                # except Exception as e:
                #     pass
                # try:
                #     # browser = await browser.new_context(proxy={"server": "http://92.61.96.231:61234:isp2536:QwQyodQYdMdh"})
                #     pass
                # except Exception as e:
                #     pass
                
                page = await browser.new_page()
                await page.goto(base_url)
                
                # Wait for the div to appear on the page
                await page.wait_for_selector('.easy-autocomplete')
                
                # Get the input element and type the search URL into it
                await page.type('.easy-autocomplete input', f'{search_url}')
                
                # Press "Enter" key
                await page.press('.easy-autocomplete input', 'Enter')
                
                # Wait for the results counter paragraph to appear
                try:
                    await page.wait_for_selector('p.results-counter')
                    result = "Yes"
                except Exception as e:
                    pass  # No need to change the default result, it's already "No"
                
                await browser.close()
        
        return result

async def main():
    # Get current date
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Read URLs from domain.txt
    with open('domain.txt', 'r') as file:
        urls = file.readlines()

    # Initialize the scraper
    scraper = PlayWrightScraper()
    
    # Open CSV file for writing
    with open(f'results_{current_date}.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Domain', 'Result'])
        
        # Iterate over each URL and perform the search
        for url in urls:
            url = url.strip()  # Remove leading/trailing whitespace and newline characters
            print(url)
            result = await scraper.search(url)
            writer.writerow([current_date, url, result])


# Run the main function
asyncio.run(main())
