import json
import time
import random
from datetime import datetime, timedelta

# Keyword-based sentiment analysis
POSITIVE_KEYWORDS = ["funding", "partnership", "breakthrough", "launch", "expansion", "growth", "approved", "innovative", "new", "revenue", "profit"]
NEGATIVE_KEYWORDS = ["layoff", "lawsuit", "declined", "failure", "crisis", "cut", "warning", "investigation", "dropped", "bankruptcy"]

def load_companies(filename='companies.json'):
    with open(filename, 'r') as f:
        return json.load(f)

def calculate_heat_score(headlines):
    score = 50 
    for headline in headlines:
        headline_lower = headline.lower()
        for pos in POSITIVE_KEYWORDS:
            if pos in headline_lower:
                score += 5
        for neg in NEGATIVE_KEYWORDS:
            if neg in headline_lower:
                score -= 7
    return max(0, min(100, score))

def fetch_mock_news(company_name, days=30):
    """
    Simulates news volume based on the number of days.
    More days = more historical context and more headlines.
    """
    # Base news volume scales with days (roughly 1 headline per 7-10 days)
    count = max(1, min(15, days // 7))
    
    possible_headlines = [
        f"{company_name} announces major funding round for AI diagnostics.",
        f"Layoffs reported at {company_name} as restructuring begins.",
        f"{company_name} partners with Mayo Clinic for robotic surgery.",
        f"Regulatory warning issued to {company_name} over data privacy.",
        f"{company_name} launches new telehealth platform in Europe.",
        f"Quarterly earnings for {company_name} exceed analyst expectations.",
        f"Legal battle looms for {company_name} over patent infringement.",
        f"New patent filed by {company_name} for AI-driven imaging.",
        f"CEO of {company_name} speaks at Global Health Summit on AI future.",
        f"Stock price of {company_name} surges after clinical trial success.",
        f"{company_name} acquisition rumors circulate in the tech sector.",
        f"New clinical study validates {company_name}'s core technology.",
        f"Executive departure at {company_name} signals strategic shift.",
        f"{company_name} expands operations to Asian markets.",
        f"Industry award granted to {company_name} for medical innovation."
    ]
    
    num_to_pick = random.randint(1, count + 1)
    num_to_pick = min(num_to_pick, len(possible_headlines))
    
    return random.sample(possible_headlines, num_to_pick)

def run_analysis(days=30):
    companies = load_companies()
    results = []
    
    for company in companies:
        name = company['name']
        news = fetch_mock_news(name, days)
        heat_score = calculate_heat_score(news)
        
        company_data = company.copy()
        company_data['latest_headlines'] = news
        company_data['heat_score'] = heat_score
        company_data['days_tracked'] = days
        company_data['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        results.append(company_data)
        
    with open('companies_with_sentiment.json', 'w') as f:
        json.dump(results, f, indent=2)
    return results

if __name__ == "__main__":
    import sys
    d = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    print(f"Running Analysis for timeframe: {d} days")
    run_analysis(d)
    print("Done.")
