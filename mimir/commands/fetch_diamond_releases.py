from flask.cli import AppGroup

import click

from ..cronjobs.fetch_diamond_releases import fetch_diamond_releases

diamond_cli = AppGroup('diamond')

@diamond_cli.command('fetch')
@click.argument('date_string', nargs=-1)
def fetch_diamond_releases_command(date_string):
  date_string = date_string[0]
  fetch_diamond_releases(date_string)
