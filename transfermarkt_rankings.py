"""!
@brief Moduł do pobierania i przetwarzania rankingu FIFA z Transfermarkt

Moduł zawiera funkcje do:
- Pobierania pełnego rankingu 211 drużyn narodowych
- Normalizacji nazw krajów
- Wyszukiwania pozycji konkretnych drużyn

@requires requests
@requires bs4.BeautifulSoup

"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict

def get_full_rankings() -> List[Dict[str, str]]:
    """!
    @brief Pobiera pełny ranking FIFA ze strony Transfermarkt

    @details Wykonuje następujące kroki:
    1. Łączy się z główną stroną rankingu
    2. Określa liczbę podstron z rankingiem
    3. Iteracyjnie pobiera dane ze wszystkich stron
    4. Parsuje dane przy użyciu BeautifulSoup

    @return List[Dict] Lista słowników z danymi drużyn w formacie:


    @throws Exception W przypadku problemów z połączeniem lub parsowaniem

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
    """!
    @brief Normalizuje nazwę kraju do standardowej formy angielskiej

    @details Wykonuje następujące operacje:
    1. Konwersja na małe litery
    2. Mapowanie znanych nazw lokalnych na angielskie
    3. Kapitalizacja pierwszej litery

    @param name str Oryginalna nazwa kraju
    @return str Znormalizowana nazwa kraju


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
    """!
    @brief Wyszukuje pozycję drużyny w rankingu FIFA

    @param team_name str Nazwa drużyny do wyszukania
    @param rankings List[Dict] Pełna lista rankingowa z get_full_rankings()
    @return int Pozycja w rankingu

    @retval 211 Jeśli drużyna nie zostanie znaleziona w rankingu



    """
    normalized_name = normalize_country_name(team_name)

    for team in rankings:
        if team['country'].lower() == normalized_name.lower():
            return team['rank']

    return 211