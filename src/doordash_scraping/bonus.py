import asyncio
from dotenv import load_dotenv
import os

from scrapybara import Scrapybara
from undetected_playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
import json

load_dotenv()
api_key = os.getenv('API_KEY')

async def get_scrapybara_browser():
    client = Scrapybara(api_key=api_key)
    instance = client.start_browser()
    return instance

class Demonstrations:
	x = 1

def generate_script(demonstrations: list[Demonstrations]) -> str:
	"""
	:args:
	demonstrations: a list of demonstration data, defined above
	
	:desc:
	consumes the demonstration data and uses LLM calls to convert it into a
	python playwright script. challenges: how to make sure its robust
	and reliable? 
	
	:returns:
	a python script
	
	Pseudocode:
	from openai import OpenAI
	client = OpenAI()

	snapshot = 0

	template  = "Write a script in python using Playwright to perform the following sequence of tasks. Do not wrap the code in a function. Assume that the page has already been initialized in a variable named 'page'. Only provide the code without further explanations:

			Action: 
			{action_string}

			Subtasks:
			{subtask_string}

			Summary:
			{transition_string}

			The HTML before and after each subtask is attached:"

	script = ""
	
	for demonstration in demonstrations:
		files = ""
		subtask_string = ""
		for subtask in subtasks:
			concat subtask to subtask_string
			concat page.wait_for_timeout(subtask["end_timestamp"] - next_subtask["begin_timestamp"]) to subtask_string
			attach before_state html and after_state html
			go to next snapshot
		form_prompt(action_string, subtask_string, transition_string)
		partial_script = callToChatGPT(prompt = prompt)
		script += partial_script
	"""

	pass

async def sample():
	instance = await get_scrapybara_browser()
	cdp_url = instance.get_cdp_url().cdp_url
	async with async_playwright() as p:
		browser = await p.chromium.connect_over_cdp(cdp_url)
		page = await browser.new_page()
		# Navigate to UberEats
		# Navigate to UberEats
		await page.goto("https://www.ubereats.com/")

		# Wait for timeout (7102 - 6493 ms)
		await page.wait_for_timeout(609)

		# Close the location access modal
		await page.wait_for_selector('[data-testid="close-button"]', timeout=5000)
		await page.click('[data-testid="close-button"]')

		# Click on the delivery address input field
		await page.click('[data-testid="location-typeahead-input"]')

		# Type '2390 el camino real' into the delivery address input field
		await page.fill('[data-testid="location-typeahead-input"]', '2390 el camino real')

		# Wait for the suggested address to appear and click on it
		await page.wait_for_selector('li:has-text("2390 El Camino Real")', timeout=5000)
		await page.click('li:has-text("2390 El Camino Real")')

if __name__ == "__main__":
    asyncio.run(sample())