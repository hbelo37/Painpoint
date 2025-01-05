import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time

def get_random_headers():
    ua = UserAgent()
    return {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }

def scrape_techcrunch(company_name):
    """Scrape news about the company using NewsAPI"""
    try:
        # Get your free API key from https://newsapi.org/register
        api_key = "04ed025422ac44e5a242e7dee5c1d184"  # Replace with your actual API key
        
        query = f'"{company_name}" AND (problem OR issue OR challenge OR controversy)'
        url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}&language=en&sortBy=relevancy&pageSize=10"
        
        response = requests.get(url)
        print(f"NewsAPI Response Status: {response.status_code}")
        
        if response.status_code == 200:
            articles = []
            data = response.json()
            
            for article in data.get('articles', []):
                title = article.get('title', '')
                description = article.get('description', '')
                
                if company_name.lower() in (title + description).lower():
                    articles.append({
                        'title': title,
                        'description': description
                    })
            return articles
        return []
    except Exception as e:
        print(f"Error in scraping news: {e}")
        return []

def scrape_glassdoor(company_name):
    """Scrape news about company issues as an alternative to Glassdoor"""
    try:
        api_key = "04ed025422ac44e5a242e7dee5c1d184"
        
        # More specific query for internal issues
        query = f'"{company_name}" AND (employee OR workplace OR "working conditions" OR management OR layoffs)'
        url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}&language=en&sortBy=relevancy&pageSize=10"
        
        response = requests.get(url)
        if response.status_code == 200:
            articles = []
            data = response.json()
            
            for article in data.get('articles', []):
                title = article.get('title', '')
                description = article.get('description', '')
                
                # Only include articles that actually mention the company
                if company_name.lower() in (title + description).lower():
                    articles.append({
                        'title': title,
                        'description': description
                    })
            return articles
        return []
    except Exception as e:
        print(f"Error in scraping company issues: {e}")
        return []
