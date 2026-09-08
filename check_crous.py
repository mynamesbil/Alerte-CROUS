import requests
import os
import json

# ============================================================
# 1) Colle ici l'URL de recherche CROUS filtrée sur "Mermoz"
#    ou "Claudie Haigneré" (voir instructions pour l'obtenir).
# ============================================================
SEARCH_URL = "https://trouverunlogement.lescrous.fr/tools/47/search?bounds=4.7718134_45.8082628_4.8983774_45.7073666&locationName=Lyon"

# Le(s) mot(s)-clé(s) à repérer dans la page de résultats.
# On s'arrête avant le "é" final de Haigneré pour que ça marche
# que le site affiche "Haigneré" (avec accent) ou "HAIGNERE" (sans accent).
KEYWORD = "JUSSIEU"

# Choisis un nom de "topic" ntfy.sh unique et difficile à deviner.
# C'est ce qui permet de recevoir les notifs sur ton téléphone.
NTFY_TOPIC = "REZMERMOZ6767"
STATE_FILE = "state.json"


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"found": False}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def notify(message):
    requests.post(
        f"https://ntfy.sh/{NTFY_TOPIC}",
        data=message.encode("utf-8"),
        headers={
            "Title": "Va postuler mon ptit shlag".encode("utf-8"),
            "Priority": "urgent",
            "Tags": "house,rotating_light",
        },
        timeout=30,
    )


def check():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        )
    }
    r = requests.get(SEARCH_URL, headers=headers, timeout=30)
    r.raise_for_status()

    found = KEYWORD.lower() in r.text.lower()
    state = load_state()

    print(f"Résultat trouvé : {found} (précédemment : {state.get('found')})")

    if found and not state.get("found"):
        notify(
            f"Félicitations mgl '{KEYWORD}' est apparu "
            f"allez cavale vite: {SEARCH_URL}"
        )
        print("Notification envoyée !")

    state["found"] = found
    save_state(state)


if __name__ == "__main__":
    check()
