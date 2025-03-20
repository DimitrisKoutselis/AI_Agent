import os
from dotenv import load_dotenv
import requests

load_dotenv('/home/grundy/PycharmProjects/diplo/.env')
api_key = os.getenv('NEWS_API_KEY')
base_url = "https://newsapi.org/v2/"

if not api_key:
    raise ValueError("NEWS_API_KEY not found in environment variables")


def get_top_news(country: str = "us", category: str = "general", page: int = 1) -> dict:
    url = f"{base_url}top-headlines"
    headers = {
        'x-api-key': api_key
    }
    params = {
        'country': country,
        'category': category,
        'page': page
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        return {"error": f"API request failed with status code {response.status_code}. Response: {response.text}"}

    try:
        data = response.json()
        return {"articles": format_news_response(data)}
    except requests.exceptions.JSONDecodeError:
        return {"error": f"Unable to parse JSON response. Response content: {response.text}"}


def get_news_by_keywords(keywords: str, language: str='en', page: int = 1) -> dict:
    url = f"{base_url}everything"
    headers = {
        'x-api-key': api_key
    }
    params = {
        'q': keywords,
        'page': page,
        'language': language,
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code!= 200:
        return {"error": f"API request failed with status code {response.status_code}. Response: {response.text}"}

    try:
        data = response.json()
        return {"articles": format_news_response(data)}
    except requests.exceptions.JSONDecodeError:
        return {"error": f"Unable to parse JSON response. Response content: {response.text}"}


def format_news_response(news_data:str) -> str:
    if "error" in news_data:
        return news_data["error"]

    articles = news_data.get("articles", [])
    if not articles:
        return "No news articles found."

    formatted_news = "Top News Articles:\n"
    for article in articles:
        title = article.get("title", "No title")
        description = article.get("description", "No description")
        url = article.get("url", "No URL")

        formatted_news += (
            f"\nTitle: {title}\n"
            f"Description: {description}\n"
            f"URL: {url}\n"
            "-------------------------"
        )

    return formatted_news.strip()


if __name__ == "__main__":
    keyword_news = get_news_by_keywords(keywords="+\"Artificial Intelligence\"")
    print('\nNews by keywords:')
    print(format_news_response(keyword_news))