import requests
from bs4 import BeautifulSoup
import cloudscraper
from telegram import Bot
import asyncio

TELEGRAM_BOT_TOKEN = "7999751443:AAGnzhygvn5LZFEJVQHaLaVhPuO5gsUZLeY"
TELEGRAM_CHAT_ID = "@war_newsx"

async def send_telegram_message(message):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

def scrape_aljazeera():
    url = "https://www.aljazeera.net/news/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    articles = []
    for link in soup.find_all('a', class_='u-clickable-card__link'):
        title = link.text.strip()
        href = link.get('href')
        if title and href:
            articles.append({'title': title, 'url': url + href if href.startswith('/') else href})
    return articles

def filter_military_news(articles):
    keywords = [
        "حرب", "عسكري", "جيش", "صراع", "نزاع", "قتال", "قصف", "صاروخ", "طائرة حربية",
        "دبابة", "سلاح", "اشتباك", "هجوم", "دفاع", "احتلال", "تحرير", "شهيد", "ضحايا",
        "إسرائيل", "فلسطين", "غزة", "القدس", "الضفة الغربية", "إيران", "أمريكا", "روسيا",
        "أوكرانيا", "سوريا", "اليمن", "لبنان", "حزب الله", "حماس", "جهاد", "إرهاب", "داعش",
        "قوات", "كتائب", "لواء", "فيلق", "جبهة", "معركة", "عملية عسكرية", "تهديد", "عقوبات",
        "اتفاقية سلام", "هدنة", "وقف إطلاق النار", "مفاوضات", "أمن", "استخبارات", "تجسس",
        "انفجار", "اغتيال", "انقلاب", "تمرد", "ثورة", "لاجئين", "نزوح", "حصاد", "خسائر",
        "دمار", "إغاثة", "مساعدات إنسانية", "مجاعة", "حصاد", "تدمير", "عنف", "توتر", "تصعيد"
    ]
    filtered_articles = []
    for article in articles:
        for keyword in keywords:
            if keyword in article['title']:
                filtered_articles.append(article)
                break # Move to the next article once a keyword is found
    return filtered_articles

async def main():
    print("Scraping Al Jazeera...")
    aljazeera_articles = scrape_aljazeera()
    print(f"Found {len(aljazeera_articles)} articles from Al Jazeera.")

    print("Filtering military and war-related news...")
    military_news = filter_military_news(aljazeera_articles)
    print(f"Found {len(military_news)} military and war-related articles.")

    for article in military_news:
        message = f"Title: {article['title']}\nURL: {article['url']}"
        print(message)
        await send_telegram_message(message)
        print("---")

if __name__ == '__main__':
    asyncio.run(main())
