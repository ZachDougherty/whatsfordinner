from recipe_scrapers import scrape_me, WebsiteNotImplementedError
from bs4 import BeautifulSoup
import requests
import os
import sys

def get_recipe(url: str):
	"Get recipe information"
	try:
		scraper = scrape_me(url)
		recipe = {
			'title': scraper.title(),
			'total_time': scraper.total_time(),  # minutes
			'yields': scraper.yields(),
			'ingredients': scraper.ingredients(),  # list
			'instructions': scraper.instructions().split('\n'),  # list
			'image': scraper.image(),  # url to image
			'host': scraper.host(),  # host website
			'url': url  # original url
		}
	except WebsiteNotImplementedError as e:
		return str(e)
	except Exception as e:
		return str(e)

	return recipe
