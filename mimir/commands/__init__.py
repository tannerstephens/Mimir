from flask import Flask

from .fetch_diamond_releases import diamond_cli

def register_commands(app: Flask):
  app.cli.add_command(diamond_cli)
