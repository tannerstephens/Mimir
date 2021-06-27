from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from flask import current_app
from html import unescape

from ..models import Distributor, Publisher, Series, Release, db_commit

import requests

DISTRIBUTOR_NAME = 'Diamond Comic Distributors'
PREVIEWS_WORLD_BASE_URL = 'https://www.previewsworld.com'
LOWRES_IMAGE_URL_FORMAT = 'https://www.previewsworld.com/SiteImage/CatalogThumbnail/{image_id}'
HIGHRES_IMAGE_URL_FORMAT = 'https://www.previewsworld.com/SiteImage/MainImage/{image_id}'
SERIES_URL_FORMAT = 'https://www.previewsworld.com/Catalog/Series/{series_id}'

def fetch_diamond_releases():
  distributorModel = Distributor.query.filter_by(name=DISTRIBUTOR_NAME).first()

  if distributorModel is None:
    distributorModel = Distributor(
      name=DISTRIBUTOR_NAME,
      lowres_image_url_format=LOWRES_IMAGE_URL_FORMAT,
      highres_image_url_format=HIGHRES_IMAGE_URL_FORMAT,
      series_url_format=SERIES_URL_FORMAT).save(False)

  current_app.logger.info('Fetching latest diamond releases')
  print('Fetching latest diamond releases')

  session = requests.session()

  all_new_releases_text = session.get(f'{PREVIEWS_WORLD_BASE_URL}/NewReleases').text
  all_new_releases_soup = BeautifulSoup(all_new_releases_text, 'html.parser')

  release_date_text = all_new_releases_soup.find('div', {'class': 'nrCurDate'}).contents[1]
  release_date = datetime.strptime(release_date_text, '%B %d, %Y')

  if(distributorModel.last_release != None and distributorModel.last_release >= release_date):
    current_app.logger.info('No new releases yet')
    print('No new releases yet')

    return

  new_releases_soup = all_new_releases_soup.find_all('div', {'class': 'nrGalleryItem'})

  for new_release_soup in new_releases_soup:
    title = unescape(new_release_soup.find('div', {'class': 'nrGalleryItemTitle'}).text)

    img_soup = new_release_soup.find('img')
    img_src = img_soup['data-src'] if img_soup.has_attr('data-src') else img_soup['src']
    image_id = img_src.split('/')[-1]

    publisher = new_release_soup.find('div', {'class': 'nrGalleryItemPublisher'}).text
    release_id = new_release_soup.find('div', {'class': 'nrGalleryItemDmdNo'}).text

    release_page_url = new_release_soup.find('div', {'class': 'nrGalleryItemDmdNo'}).find('a')['href']
    release_page_text = session.get(f'{PREVIEWS_WORLD_BASE_URL}{release_page_url}').text
    release_page_soup = BeautifulSoup(release_page_text, 'html.parser')
    series_soup = release_page_soup.find('a', {'class': 'btn ViewSeriesItemsLink'})
    series_id = series_soup['href'].split('/')[-1] if series_soup else None

    publisherModel = Publisher.query.filter_by(name=publisher).first()

    if publisherModel is None:
      publisherModel = Publisher(name=publisher).save(False)

    if series_id is not None:
      seriesModel = Series.query.filter_by(series_id=series_id).first()

      if seriesModel is None:
        series_page_text = session.get(SERIES_URL_FORMAT.format(series_id=series_id)).text
        series_page_soup = BeautifulSoup(series_page_text, 'html.parser')
        series_title = ' '.join(series_page_soup.find('div', {'class': 'Title'}).text.split(' ')[1:])

        seriesModel = Series(title=series_title, series_id=series_id).save(False)
    else:
      seriesModel = None

    Release(
      title=title,
      image_id=image_id,
      publisher=publisherModel,
      release_id=release_id,
      series=seriesModel,
      distributor=distributorModel).save(False)

  distributorModel.last_release = release_date
  distributorModel.save()

  db_commit()
