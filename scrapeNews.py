import requests
from bs4 import BeautifulSoup


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
    heading = soup.find(id="uamods-topics")

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
    while(True):
        pageUrl = url + "?page=" + str(pageNumber)
        html_doc = requests.get(pageUrl).text
        soup = BeautifulSoup(html_doc, 'lxml')
        text = soup.select("div>div>main>div>div>article>div")[
            0].get_text()
        textList.append(text)

        if not hasYahooNextPage(pageUrl, soup):
            title = soup.select("#uamods>header>h1")[0].get_text()
            break
        pageNumber += 1

    return {"title": title, "textList": textList}


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


if __name__ == "__main__":
    heading = getYahooHeading()[0]["url"]
    article = getYahooArticleFromPickUp(heading)
    articleTextList = getYahooArticleText(article)
    print(articleTextList)
