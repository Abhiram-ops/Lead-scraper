import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
import re

# Set your SerpAPI key here (create an account at serpapi.com and get a free key)
SERPAPI_KEY = "your_serpapi_api_key"

# Function to extract emails and phones from a page
def extract_contacts_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()

        emails = set(re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text))
        phones = set(re.findall(r"\+?\d[\d -]{8,}\d", text))

        return list(emails), list(phones)
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return [], []

# Function to search for leads using Google
def search_leads(query, num_pages=1):
    all_leads = []

    for page in range(num_pages):
        params = {
            "engine": "google",
            "q": query,
            "api_key": SERPAPI_KEY,
            "start": page * 10
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        for result in results.get("organic_results", []):
            link = result.get("link")
            title = result.get("title", "")
            snippet = result.get("snippet", "")
            if link:
                print(f"Scraping {link}")
                emails, phones = extract_contacts_from_url(link)

                if emails or phones:
                    all_leads.append({
                        "url": link,
                        "title": title,
                        "snippet": snippet,
                        "emails": emails,
                        "phones": phones
                    })

    return all_leads

# Example usage
if __name__ == "__main__":
    # Define your niche
    niche = "digital marketing agencies in India contact"

    leads = search_leads(niche, num_pages=2)

    # Print results
    for idx, lead in enumerate(leads, start=1):
        print(f"\nLead {idx}:")
        print(f"URL: {lead['url']}")
        print(f"Title: {lead['title']}")
        print(f"Emails: {lead['emails']}")
        print(f"Phones: {lead['phones']}")
