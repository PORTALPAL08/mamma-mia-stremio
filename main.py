import os
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Questo risolve molti problemi di "Failed to fetch" su Stremio Web

# Funzione per recuperare il nome del film dall'ID IMDb (es. tt12345)
def get_movie_name(imdb_id):
    try:
        # Usiamo l'API di Cinemeta (Stremio) per tradurre tt... in un titolo
        r = requests.get(f"https://v3-cinemeta.strem.io/meta/movie/{imdb_id}.json", timeout=5)
        if r.status_code == 200:
            return r.json().get('meta', {}).get('name')
        return None
    except:
        return None

@app.route('/')
def index():
    return "Mamma Mia Addon is Online! Copy this URL into Stremio: /manifest.json"

@app.route('/manifest.json')
def manifest():
    return jsonify({
        "id": "org.lucas.mammamiamulti.ita",
        "version": "1.0.0",
        "name": "Mamma Mia ITA",
        "description": "Cerca su StreamingCommunity e Tantifilm (No Torrent)",
        "resources": ["stream"],
        "types": ["movie", "series"],
        "idPrefixes": ["tt"]
    })

@app.route('/stream/<type>/<id>.json')
def stream(type, id):
    # Rimuoviamo eventuali suffissi per le serie TV (es. tt123:1:1 -> tt123)
    imdb_id = id.split(':')[0]
    title = get_movie_name(imdb_id)
    streams = []
    
    if title:
        # Prepariamo il titolo per gli URL (spazi diventano +)
        clean_title = title.replace(" ", "+")
        
        # Link StreamingCommunity
        streams.append({
            "name": "Mamma Mia",
            "title": f"🎬 StreamingCommunity\n{title}",
            "externalUrl": f"https://streamingcommunity.bet/search?q={clean_title}"
        })
        
        # Link Tantifilm
        streams.append({
            "name": "Mamma Mia",
            "title": f"🍿 Tantifilm\n{title}",
            "externalUrl": f"https://www.tantifilm.rent/?s={clean_title}"
        })

    return jsonify({"streams": streams})

if __name__ == '__main__':
    # Render usa la variabile PORT, altrimenti usa la 10000 di default
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
