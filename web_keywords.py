import requests
import certifi
from bs4 import BeautifulSoup

def search_duckduckgo(query):
    """
    Search DuckDuckGo and return the HTML content of the page.
    :param query: The search query.
    :return: HTML content of the search result page.
    """
    url = f"https://duckduckgo.com/html/?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers, verify=certifi.where())
    response.raise_for_status()
    return response.text

def parse_results(html, keywords):
    """
    Parse the HTML content and extract search results that match the keywords.
    :param html: HTML content of the search result page.
    :param keywords: Keywords to filter the search results.
    :return: List of dictionaries containing filtered search results.
    """
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

def search_and_display_keywords(keywords, num_results=5, display_format='detailed'):
    """
    Search DuckDuckGo for the given keywords and display the results.
    :param keywords: A list of keywords for the search query.
    :param num_results: Number of search results to display.
    :param display_format: The format for displaying the results ('detailed' or 'summary').
    """
    
    query = "+".join(keywords)
    html = search_duckduckgo(query)
    results = parse_results(html, keywords)
    
    if not results:
        print("No results found.")
        return

    if display_format == 'detailed':
        for i, result in enumerate(results[:num_results], 1):
            print(f"Result {i}:")
            print("Title:", result["title"])
            print("Description:", result["description"])
            print("Link:", result["link"])
            print("--------------------")
    
    elif display_format == 'summary':
        for i, result in enumerate(results[:num_results], 1):
            print(f"Result {i}: {result['title']} - {result['link']}")

# Example usage for separate searches
print("Search Results for 'Common Vulneribilites for Python':")
search_and_display_keywords(["update","python"], num_results=10, display_format='summary')

print("\nSearch Results for 'Common Vulneribilites for ekmek:")
search_and_display_keywords(["CVE","Ekmek"], num_results=10, display_format='summary')

print("\nSearch Results for 'Common Vulneribilites for kurt:")
search_and_display_keywords(["CVE","kurt"], num_results=10, display_format='summary')



