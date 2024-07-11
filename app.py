from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import random
import time
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
CORS(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["20 per minute"]
)

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
]

def search_entity(entity_name):
    search_url = f"https://offshoreleaks.icij.org/search?q={entity_name}&c=&j=&d="
    
    headers = {
        "User-Agent": random.choice(user_agents)
    }
    
    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        return {"error": f"Error realizando la solicitud: {str(e)}"}
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    table = soup.find('table')
    
    if not table:
        return {"error": "No se encontraron resultados para la entidad especificada."}
    
    rows = []
    for row in table.find_all('tr')[1:]:  
        columns = row.find_all('td')
        if len(columns) >= 4:
            entity = columns[0].text.strip()
            jurisdiction = columns[1].text.strip()
            linked_to = columns[2].text.strip()
            data_from = columns[3].text.strip()
            rows.append({
                "Entity": entity,
                "Jurisdiction": jurisdiction,
                "LinkedTo": linked_to,
                "DataFrom": data_from
            })
    
    results = {
        "hits": len(rows),
        "rows": rows
    }
    return results

@app.route('/search', methods=['GET'])
@limiter.limit("20 per minute")
def search():
    entity_name = request.args.get('entity_name')
    if not entity_name:
        return jsonify({"error": "Se requiere el parámetro 'entity_name'."}), 400
    
    time.sleep(random.uniform(1, 3))
    
    results = search_entity(entity_name)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
