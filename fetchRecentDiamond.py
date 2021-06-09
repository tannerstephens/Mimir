import html
import json
import requests_cache

from bs4 import BeautifulSoup
from typing import Any

PREVIEWS_WORLD_BASE_URL = 'https://www.previewsworld.com'

class Release:
  def __init__(self, title, image_id, publisher, release_id, series_id) -> None:
    self.title = title
    self.image_id = image_id
    self.publisher = publisher
    self.release_id = release_id
    self.series_id = series_id

  def __repr__(self) -> str:
    return self.name

  def to_dict(self) -> dict:
    return {
      'title': self.title,
      'image_id': self.image_id,
      'publisher': self.publisher,
      'release_id': self.release_id,
      'series_id': self.series_id
    }

class ReleaseEncoder(json.JSONEncoder):
  def default(self, obj: Any) -> Any:
    if(isinstance(obj, Release)):
      return obj.to_dict()
    else:
      return json.JSONEncoder.default(self, obj)

def fetch_series_id(release_soup: BeautifulSoup, session):
  release_page = release_soup.find('div', {'class': 'nrGalleryItemDmdNo'}).find('a')['href']

  release_page_text = session.get(f'{PREVIEWS_WORLD_BASE_URL}{release_page}').text

  release_page_soup = BeautifulSoup(release_page_text, 'html.parser')
  series_soup = release_page_soup.find('a', {'class': 'btn ViewSeriesItemsLink'})

  if series_soup:
    series_url_part = series_soup['href']
    return series_url_part.split('/')[-1]

  return None

def main():
  session = requests_cache.CachedSession('previewsWorld')
  with session.cache_disabled():
    new_releases_text = session.get(f'{PREVIEWS_WORLD_BASE_URL}/NewReleases').text

  soup = BeautifulSoup(new_releases_text, 'html.parser')

  releases_soup = soup.find_all('div', {'class': 'nrGalleryItem'})

  releases = []

  for release_soup in releases_soup:
    title = html.unescape(release_soup.find('div', {'class': 'nrGalleryItemTitle'}).text)

    img_soup = release_soup.find('img')

    if(img_soup.has_attr('data-src')):
      img_src = img_soup['data-src']
    else:
      img_src = img_soup['src']

    image_id = img_src.split('/')[-1]
    publisher = release_soup.find('div', {'class': 'nrGalleryItemPublisher'}).text
    release_id = release_soup.find('div', {'class': 'nrGalleryItemDmdNo'}).text

    series_id = fetch_series_id(release_soup, session)

    print(title, series_id)

    release = Release(title, image_id, publisher, release_id, series_id)

    releases.append(release)

  with open('output.json', 'w') as f:
    json.dump(releases, f, cls=ReleaseEncoder, indent=4)

if __name__ == '__main__':
  main()
