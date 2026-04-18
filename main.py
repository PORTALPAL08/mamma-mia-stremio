import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# Funzione per recuperare il nome del film usando l'ID IMDb (es. tt12345)
def get_movie_name(imdb_id):
    try:
        # Usiamo l'API pubblica di Cinemeta (Stremio)
        r = requests.get(f"https://v3-cinemeta.strem.io/meta/movie/{imdb_id}.json", timeout=5)
        return r.json().get('meta', {}).get('name')
    except:
        return None

@app.route('/')
def index():
    return "Mamma Mia Addon is Online! Use /manifest.json to install it on Stremio."

@app.route('/manifest.json')
def manifest():
    return jsonify({
        "id": "org.lucas.mammamiamulti",
        "version": "1.0.0",
        "name": "Mamma Mia ITA",
        "description": "No-Torrent: StreamingCommunity & Tantifilm",
        "resources": ["stream"],
        "types": ["movie", "series"],
        "idPrefixes": ["tt"]
    })

@app.route('/stream/<type>/<id>.json')
def stream(type, id):
    title = get_movie_name(id)
    streams = []
    
    if title:
        # Prepariamo il titolo per la ricerca (sostituiamo gli spazi con +)
        clean_title = title.replace(" ", "+")
        
        # Sorgente 1: StreamingCommunity
        streams.append({
            "name": "Mamma Mia",
            "title": f"🎬 StreamingCommunity\n{title}",
            "externalUrl": f"https://streamingcommunity.bet/search?q={clean_title}"
        })
        
        # Sorgente 2: Tantifilm
        streams.append({
            "name": "Mamma Mia",
            "title": f"🍿 Tantifilm\n{title}",
            "externalUrl": f"https://www.tantifilm.rent/?s={clean_title}"
        })

    return jsonify({"streams": streams})

if __name__ == '__main__':
    # Render assegna una porta dinamica tramite la variabile d'ambiente PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
