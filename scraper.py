import os
import datetime
from bs4 import BeautifulSoup
import requests
from datastructures import Article
import scraperwiki

REST_URL: str = "https://www.polizei.bayern.de/es/search"
BASE_URL: str = "https://www.polizei.bayern.de"

query = {
    "params": {
        "type": "presse",
        "q": '{"queryStr":false,"datefr":"14.06.2022","dateto":"15.06.2022","author":null}',
    }
}

response = requests.post(REST_URL, json=query)

for hit in response.json()["hits"]["hits"]:
    content = hit["_source"]
    title = content["title"]
    date = datetime.datetime.strptime(content["created_date"], "%d.%m.%Y")
    id = "pby_" + content["directory"].split("/")[-1]
    location = content["creating_organization"]
    source = BASE_URL + content["directory"]

    print(f"Downloading article {source}.")
    article_page = BeautifulSoup(requests.get(source).text, features="html.parser")
    text = article_page.find("section", {"class": "bp-textblock-image"}).text.strip()

    article = Article(
        id=id, title=title, content=text, location=location, date=date, source=source
    )

    scraperwiki.sqlite.save(unique_keys=["id"], data=article.dict())

os.rename("scraperwiki.sqlite", "data.sqlite")