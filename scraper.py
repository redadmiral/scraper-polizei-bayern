import os
import datetime
from bs4 import BeautifulSoup
import requests
from datastructures import Article
import scraperwiki

REST_URL: str = "https://www.polizei.bayern.de/es/search"
BASE_URL: str = "https://www.polizei.bayern.de/"

today = datetime.datetime.now()
yesterday = today - datetime.timedelta(hours=24)

today_str = datetime.datetime.strftime(today, "%d.%m.%Y")
yesterday_str = datetime.datetime.strftime(yesterday, "%d.%m.%Y")

query = {
    "params": {
        "type": "presse",
        "q": f'{{"queryStr":false,"datefr":"{yesterday_str}","dateto":"{today_str}","author":null}}',
    }
}

response = requests.post(REST_URL, json=query, verify=False)

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