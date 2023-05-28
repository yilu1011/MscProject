import json
import re
from textdistance import DamerauLevenshtein

word_distance = DamerauLevenshtein()

def get_closest(iterable, word: str, max_distance: int=None):
    _argmin, _min = None, None
    for w in iterable:
        d = word_distance(w, word)
        if _min is None or _min > d:
            if max_distance is None or d <= max_distance:
                _argmin, _min = w, d
    return _argmin

def parse_date(date: str):
    date = re.sub(r'\W+', " ", date.strip())
    details = date.split(" ")

    if len(details) != 3 or "?" in date:
        return date

    mois = {
        "janvier": "01",
        "fevrier": "02",
        "mars": "03",
        "avril": "04",
        "mai": "05",
        "juin": "06",
        "juillet": "07",
        "aout": "08",
        "septembre": "09",
        "octobre": "10",
        "novembre": "11",
        "decembre": "12",
    }

    mois_date = get_closest(mois, details[1], 2)
    if mois_date is None:
        return date

    return details[2] + "-" + mois[mois_date] + "-" + details[0].rjust(2,"0")

def get_spaces(line: str, allow_errors: int=0):
    espace_mentionés = []
    line = line.lower()

    with open("./data/prefix_remove.json", 'r') as f:
        prefix_regex = json.load(f)

    with open("./data/geographical_places.json", 'r') as f:
        espaces = json.load(f)
        espaces.sort(key=len, reverse=True)
        espaces = [espace.lower() for espace in espaces]

        for espace in espaces:
            for prefix in prefix_regex:
                re.sub(re.compile(prefix + espace), '', line)
            if espace in line:
                espace_mentionés.append(espace)
                line = re.sub(espace, '', line)
    return set(espace_mentionés)