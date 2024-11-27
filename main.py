"""A script that scrapes data from the Onion website."""

import requests as req
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup
import json


class OnionError(Exception):
    """Errors when accessing the Onion site."""
    pass


def get_article_details(url: str) -> dict:
    """Returns a dict of Onion article data."""
    result = req.get(url)
    if result.status_code >= 400:
        raise OnionError("Unable to access URL successfully.")
    onion_soup = BeautifulSoup(result.text, features="html.parser")
    tag_holder = onion_soup.find("div", class_="taxonomy-post_tag")
    tags = tag_holder.find_all("a") if tag_holder else []
    return {
        "title": onion_soup.find("h1").get_text(),
        "url": url,
        # datetime.fromisoformat(onion_soup.find("time")["datetime"]),
        "published": onion_soup.find("time")["datetime"],
        "tags": [tag.get_text() for tag in tags]
    }


def get_articles_from_page(url: str) -> list[dict]:
    """Returns a list of all article details on the page."""
    result = req.get(url)
    if result.status_code >= 400:
        raise OnionError("Unable to access URL successfully.")
    onion_soup = BeautifulSoup(result.text, features="html.parser")
    links = onion_soup.find_all("h3")
    articles = []
    for l in links:
        article = get_article_details(l.find("a")["href"])
        if article:
            articles.append(article)
    return articles


def main():
    all_articles = []
    for i in range(1, 5):
        all_articles.extend(
            get_articles_from_page(f"https://theonion.com/news/page/{i}/"))

    with open("onion_articles.json", "w") as f:
        json.dump(all_articles, f, indent=4)


if __name__ == "__main__":
    main()
