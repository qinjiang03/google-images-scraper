import os
import json
from requests.api import get
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()

RESULTS_DIR = './data/results'
os.makedirs(RESULTS_DIR, exist_ok=True)

queries = [row.strip().lower() for row in open('./queries.txt', 'r')]

def get_file_name(query):
    return '_'.join(query.lower().split())


for query in queries:
    print(f'Fetching for {query}...')
    params = {
        "q": query,
        "tbm": "isch",
        "ijn": "0",
        "api_key": os.environ.get('API_KEY')
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    if 'error' in results:
        print(f'Error fetching results for {query}')
        print(results['error'])
    else:
        out_file = os.path.join(RESULTS_DIR, f'{get_file_name(query)}.json')
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False)