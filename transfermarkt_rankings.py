"""
Moduł do pobierania pełnego rankingu FIFA (211 drużyn) z Transfermarkt
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict

def get_full_rankings() -> List[Dict[str, str]]:
    """
    Pobiera pełny ranking FIFA (211 drużyn) z Transfermarkt
    """
    url = "https://www.transfermarkt.com/statistik/weltrangliste"

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        rankings = []

        last_page = int(soup.find('li', class_='tm-pagination__list-item--icon-last-page').a['href'].split('=')[-1])

        for page in range(1, last_page + 1):
            if page > 1:
                response = requests.get(f"{url}?page={page}", headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')

            table = soup.find('table', {'class': 'items'})
            rows = table.find_all('tr')[1:]

            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 4:
                    rank = cols[0].text.strip()
                    country = cols[1].img['title'] if cols[1].img else cols[1].text.strip()
                    points = cols[3].text.strip().replace('.', '').replace(',', '.')

                    rankings.append({
                        'rank': int(rank),
                        'country': country,
                        'points': float(points)
                    })

        return rankings

    except Exception as e:
        print(f"Błąd podczas pobierania rankingu: {e}")
        return []

def normalize_country_name(name: str) -> str:
    """
    Normalizuje nazwę kraju do formy angielskiej z dużej litery
    """
    country_mapping = {
        'polska': 'Poland',
        'niemcy': 'Germany',
        'usa': 'United States',
        'holandia': 'Netherlands',
        'włochy': 'Italy',
        'francja': 'France',
        'hiszpania': 'Spain',
        'anglia': 'England',
        'brazylia': 'Brazil',
        'argentyna': 'Argentina'
    }
    return country_mapping.get(name.lower(), name.title())

def get_team_rank(team_name: str, rankings: List[Dict]) -> int:
    """
    Znajduje ranking dla konkretnej drużyny
    """
    normalized_name = normalize_country_name(team_name)

    for team in rankings:
        if team['country'].lower() == normalized_name.lower():
            return team['rank']

    return 211