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
    
    # Look for news items with the correct class
    for item in soup.select(".NwsLstPg_txt-cnt"):
        title_element = item.select_one(".NwsLstPg_ttl-lnk")
        if title_element:
            title = title_element.get_text(strip=True)
            link = title_element.get('href')
            
            # Get summary from the same container
            summary_element = item.select_one(".NwsLstPg_smmry")
            summary = summary_element.get_text(strip=True) if summary_element else ""
            
            if title and link:
                articles.append({
                    "title": title,
                    "summary": summary,
                    "url": link
                })
    
    return articles

def scrape_ndtv():
    url = "https://www.ndtv.com/latest"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    articles = []
    for card in soup.select(".NwsLstPg_txt-cnt"):
        title_element = card.select_one(".NwsLstPg_ttl-lnk")
        img_element = card.find_previous_sibling("a", class_="NwsLstPg_img")
        summary_element = card.select_one(".NwsLstPg_smmry")
        title = title_element.get_text(strip=True) if title_element else ""
        link = title_element.get('href') if title_element else ""
        summary = summary_element.get_text(strip=True) if summary_element else ""
        image = img_element.img['src'] if img_element and img_element.img else ""
        if title and link:
            articles.append({
                "title": title,
                "summary": summary,
                "url": link,
                "image": image
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