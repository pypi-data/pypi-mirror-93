from miniscrapes.scrapers import covid
from miniscrapes.scrapers import weather


SCRAPERS = {
    'covid': covid,
    'weather': weather
}


def run_scrapers(zip_code: str, state: str):
    results = {}
    for slug, scraper in SCRAPERS.items():
        results[slug] = scraper(zip_code, state)

    return results
