from .scraper import scrape_techcrunch, scrape_glassdoor
from .nlp_processing import extract_pain_points

def get_company_pain_points(company_name):
    # Debug prints
    print(f"\nSearching for: {company_name}")
    
    # Get data from different sources
    techcrunch_articles = scrape_techcrunch(company_name)
    print(f"TechCrunch articles found: {len(techcrunch_articles)}")
    
    glassdoor_reviews = scrape_glassdoor(company_name)
    print(f"Glassdoor reviews found: {len(glassdoor_reviews)}")
    
    # Combine all texts
    texts = techcrunch_articles + glassdoor_reviews
    
    print(f"Total texts to analyze: {len(texts)}")
    
    # Extract pain points with company context
    pain_points = extract_pain_points(texts, company_name)
    return pain_points
