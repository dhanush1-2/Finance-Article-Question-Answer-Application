import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter


def fetch_article(link):
    """Fetch and clean article text for LLM processing."""
    session = requests.Session()
    session.mount('https://', HTTPAdapter(max_retries=2))

    headers = {
        'Referer': 'https://www.moneycontrol.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = session.get(link, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Try to find article content
        article = soup.find('div', {'class': 'arti-flow'})
        if not article:
            print(f"No article content found at {link}")
            return ""

        # Remove unwanted elements
        for elem in article.find_all(['script', 'style', 'iframe', 'figure', 'div']):
            elem.decompose()

        # Focus on paragraph text
        paragraphs = article.find_all('p')
        if not paragraphs:
            text = article.get_text(strip=True)
        else:
            text = ' '.join(p.get_text(strip=True) for p in paragraphs)

        # Basic length check
        if len(text) < 100:  # Arbitrary minimum for valid article
            print(f"Article too short at {link}")
            return ""

        return text.strip()

    except requests.exceptions.RequestException as e:
        print(f"Error fetching article {link}: {e}")
        return ""
    except Exception as e:
        print(f"Unexpected error processing article {link}: {e}")
        return ""


# # Test it
# if __name__ == "__main__":
#     link = 'https://www.moneycontrol.com/news/opinion/trump-s-dollar-dilemma-12949689.html#goog_rewarded'
#     text = fetch_article(link)
#     print(text)
