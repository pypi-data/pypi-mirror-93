"""Console script for miniscrapes."""
import sys
import click

from miniscrapes.execution import run_scrapers
from miniscrapes.handlers import email_results


@click.group()
def miniscrapes(args=None):
    pass


@miniscrapes.command()
@click.option('--to', required=True, help='Miniscrape recipient email')
@click.option('--zip-code', required=True, help='Zipcode to scrape')
@click.option('--state', required=True, help='State to scrape')
def email_scrapers(to: str, zip_code: str, state: str):
    results = run_scrapers(zip_code, state)
    email_results(to, results)


if __name__ == "__main__":
    sys.exit(miniscrapes())  # pragma: no cover
