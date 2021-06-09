from bs4 import BeautifulSoup

from flask import current_app

PREVIEWS_WORLD_BASE_URL = 'https://www.previewsworld.com'

def fetch_series_id(release_soup: BeautifulSoup, session):
  release_page = release_soup.find('div', {'class': 'nrGalleryItemDmdNo'}).find('a')['href']

  release_page_text = session.get(f'{PREVIEWS_WORLD_BASE_URL}{release_page}').text

  release_page_soup = BeautifulSoup(release_page_text, 'html.parser')
  series_soup = release_page_soup.find('a', {'class': 'btn ViewSeriesItemsLink'})

  if series_soup:
    series_url_part = series_soup['href']
    return series_url_part.split('/')[-1]

  return None

def fetch_diamond_releases():
  current_app.logger.info("Fetching latest diamond releases")
