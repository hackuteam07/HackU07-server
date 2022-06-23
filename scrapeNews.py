import requests
from bs4 import BeautifulSoup
from functools import reduce
import json
import codecs


def getYahooHeading() -> list[dict[str, str]]:
    """Yahooの見出しのタイトルとURLを取得する関数

    Returns:
        list[dict[str,str]]: 見出しのタイトルとURLの辞書型のリスト
            dict[str,str]:
                title: 記事のタイトル
                url:   記事のURL
    """
    url = "https://news.yahoo.co.jp/"
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, "lxml")
    heading = soup.select_one("#uamods-topics>div>div>div>ul")

    return [{"title": link.get_text(), "url": link.get("href")} for link in heading.find_all('a')]


def getYahooArticleFromPickUp(url: str) -> str:
    """見出しから記事を開くと出てくるpickupというページから記事本文のリンクを取得する関数

    Args:
        url(str): pickupのURL

    Returns:
        str:記事本文のリンク
    """
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, "lxml")
    link = soup.select("article>div>div>p>a")[-1].get("href")
    return link


def getYahooArticleText(url: str) -> dict[str, str | list]:
    """記事本文を取得する関数

    Args:
        url(str):記事のURL

    Returns:
        dict:タイトルと、記事の本文のテキストをページごとにリストで返却
            title(str):タイトル
            textList(list[str]):ページごとの本文のリスト
    """

    pageNumber = 1
    textList = []
    title = ""
    try:
        while(True):
            pageUrl = url + "?page=" + str(pageNumber)
            html_doc = requests.get(pageUrl).text
            soup = BeautifulSoup(html_doc, 'lxml')
            for a in soup.select('a:not(.pagination_item.pagination_item-next>a)'):
                a.extract()

            # h2タグとpを区別する方　text = [{"tag":v.name ,"text":v.get_text()}   for v in soup.select(".article_body.highLightSearchTarget>div>p,h2") if not v.get_text() == '']
            text = soup.select(".article_body.highLightSearchTarget")[
                0].get_text()
            textList.append(text)

            if not hasYahooNextPage(pageUrl, soup):
                title = soup.select("#uamods>header>h1")[0].get_text()
                break
            pageNumber += 1

        return {"title": title, "textList": textList}

    except IndexError:
        return {"title": "", "textList":[""]}


def hasYahooNextPage(url: str, soup: BeautifulSoup) -> bool:
    """記事に次のページがあるか判定する関数

    Args:
        url(str): 記事のURL
        soup(BeautifulSoup): 記事のsoup
    Returns:
        bool:次のページがあればTrue,なければFalse

    """

    nextPage = soup.select(".pagination_item.pagination_item-next>a")
    return len(nextPage) != 0


def getYahooAllTopics(date):
    url = "https://news.yahoo.co.jp/topics/top-picks?date="+date
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, "lxml")
    topics = soup.select(".newsFeed_item_link")
    print(topics)
    return [{"title": link.get_text(), "url": link.get("href")} for link in topics]


if __name__ == "__main__":
    articleList = []
    for topic in getYahooHeading():

        article = getYahooArticleFromPickUp(topic["url"])
        articleTextList = getYahooArticleText(article)
        title = articleTextList["title"]
        text = reduce(lambda a, b: a+b, articleTextList["textList"])

        articleList.append({"title": title, "text": text, "url": article})
    articleListJson = json.dumps(articleList, ensure_ascii=False)
    fileName = "articleList.json"
    file = codecs.open(fileName, 'w', 'utf-8')

    file.write(articleListJson)
