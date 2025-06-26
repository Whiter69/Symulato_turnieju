"""!

@brief Moduł pomocniczy do operacji na danych turnieju

Moduł zawiera funkcje do:
- Zapis wyników turnieju do formatu JSON
- Obsługi danych turniejowych

@requires json
"""

import json

def save_results(teams, filename="data.json"):
    """!
    @brief Zapisuje wyniki turnieju do pliku w formacie JSON



    @param teams List[Team] Lista obiektów Team do zapisania
    @param filename str Nazwa pliku wyjściowego (domyślnie "data.json")

    @throws IOError W przypadku problemów z zapisem do pliku
    @post Tworzy plik JSON z danymi turniejowymi


    """
    data = [
        {
            "team": t.name,
            "fifa_ranking": t.fifa_rank,
            "punkty turnieju": t.points,
            "bramki strzelone": t.goals
        } for t in teams
    ]

    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"\nRezultat zapisany do: {filename}")
    except IOError as e:
        print(f"Błąd zapisu do pliku: {e}")