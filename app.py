from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

def scrape_ndtv():
    url = "https://www.ndtv.com/latest"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    articles = []
    for item in soup.select(".news_Itm"):
        title = item.select_one(".newsHdng")
        summary = item.select_one(".newsCont")
        link = title.a['href'] if title and title.a else None
        if title and summary and link:
            articles.append({
                "title": title.get_text(strip=True),
                "summary": summary.get_text(strip=True),
                "url": link
            })
    return articles

def scrape_bbc():
    url = "https://www.bbc.com/news"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    articles = []
    for item in soup.select("a.gs-c-promo-heading"):
        title = item.get_text(strip=True)
        link = "https://www.bbc.com" + item['href']
        if title and link:
            articles.append({
                "title": title,
                "summary": "",  # BBC homepage doesn't have summaries; you can fetch article page for more
                "url": link
            })
    return articles

@app.route('/news', methods=['GET'])
def get_news():
    source = request.args.get('source', 'ndtv')
    if source == 'bbc':
        articles = scrape_bbc()
    else:
        articles = scrape_ndtv()
    return jsonify(articles)

if __name__ == '__main__':
    app.run()