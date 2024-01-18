import requests
import certifi
from bs4 import BeautifulSoup

def search_duckduckgo(query):
    url = f"https://duckduckgo.com/html/?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers, verify=certifi.where())
    response.raise_for_status()
    return response.text

def parse_results(html, keywords):
    soup = BeautifulSoup(html, "html.parser")
    results = soup.select("div.result")
    found_results = []
    
    for result in results:
        link = result.select_one("a.result__url")
        title = result.select_one("h2.result__title")
        description = result.select_one("a.result__snippet")
        
        if link and title and description:
            link = link.get("href")
            title = title.get_text()
            description = description.get_text()
            
            if any(keyword.lower() in title.lower() or keyword.lower() in description.lower() for keyword in keywords):
                found_results.append({"title": title, "description": description, "link": link})
    
    return found_results

def search_keywords(keywords, num_results=5):
    query = "+".join(keywords)
    html = search_duckduckgo(query)
    results = parse_results(html, keywords)
    
    if results:
        for i, result in enumerate(results[:num_results], 1):
            print(f"Result {i}:")
            print("Title:", result["title"])
            print("Description:", result["description"])
            print("Link:", result["link"])
            print("--------------------")
    else:
        print("No results found.")

# Example usage
search_keywords(["ekmek","teknesi"], num_results=20)
