import requests
import sys
import json

# Windows console encoding fix
sys.stdout.reconfigure(encoding='utf-8')

APP_ID = "8ee5a987b9ec70631de1977bde3afd7ebc11140d"

def search_census_data():
    url = "http://api.e-stat.go.jp/rest/3.0/app/json/getStatsList"
    params = {
        "appId": APP_ID,
        "searchWord": "国勢調査 2020 都道府県",
        "limit": 5
    }
    
    print(f"Searching API: {url}")
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        print("\nSearch Results:")
        if "GET_STATS_LIST" in data and "DATALIST" in data["GET_STATS_LIST"]:
            tables = data["GET_STATS_LIST"]["DATALIST"]["TABLE_INF"]
            if isinstance(tables, dict):
                tables = [tables]
                
            for table in tables:
                print(f"ID: {table['@id']}")
                print(f"Stat Name: {table['STAT_NAME']['$']}")
                print(f"Title: {table['TITLE']['$']}")
                print("-" * 40)
        else:
            print("No data found or API error.")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    search_census_data()
