"""A script that scrapes data from the Onion website."""

import requests as req
from bs4 import BeautifulSoup


class OnionError(Exception):
    """Errors when accessing the Onion site."""
    pass


def get_article_info(url: str) -> dict:
    """Returns a dict of Onion article data."""
    result = req.get(url)

    if result.status_code < 400:
        onion_soup = BeautifulSoup(result.text, features="html.parser")
        return {"title": onion_soup.find("h1").get_text()}

    raise OnionError("Unable to access URL successfully.")


def get_articles_from_page(url: str) -> list[dict]:
    """Returns a list of all article details on the page."""
    pass


def main():
    return get_article_info("https://theonion.com/report-most-americans-have-enough-saved-for-absolutely-incredible-single-day-of-retirement/")


if __name__ == "__main__":
    print(main())
