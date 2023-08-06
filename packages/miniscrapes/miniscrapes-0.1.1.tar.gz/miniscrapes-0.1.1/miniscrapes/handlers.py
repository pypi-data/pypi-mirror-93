import dpath.util
import os
import requests
import textwrap

from typing import Tuple


MAILGUN_KEY = os.getenv('MAILGUN_KEY')
MAILGUN_OUTGOING_DOMAIN = os.getenv('MAILGUN_OUTGOING_DOMAIN')
EXTRACTORS = (
    ('weather', (
        ('Lo', 'today/min'),
        ('Hi', 'today/max'),
        ('Feels', 'today/feels_like'),
        ('Weather', 'today/description'))),
    ('covid', (
        ('Positive rate', 'dayPositiveRate'), ))
)


def send_simple_message(to: str, subject: str, text: str):
    requests.post(
        f'https://api.mailgun.net/v3/{MAILGUN_OUTGOING_DOMAIN}/messages',
        auth=('api', MAILGUN_KEY),
        data={
            'from': 'Miniscrapes daily email <marcua@marcua.net>',
            'to': [to],
            'subject': subject,
            'text': text}).raise_for_status()


def _extract_result(scrape: str, results: dict,
                    extractors: Tuple[Tuple[str, str], ...]) -> str:
    extracted = '\n'.join(
        f"{description}: {dpath.util.get(results, path)}"
        for description, path in extractors)
    return textwrap.dedent(f'''
    {scrape.capitalize()}
    ---
    {extracted}
    ''')


def email_results(to: str, results: dict):
    extracted = '\n\n'.join(
        _extract_result(scrape, results[scrape], extractors)
        for scrape, extractors in EXTRACTORS)
    text = textwrap.dedent(
        f'''
    Good morning! Here are your miniscrapes!

    {extracted}
    ''')
    send_simple_message(to, 'Your morning miniscrapes', text)
