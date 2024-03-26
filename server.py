import requests

API_URL = "https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22Argentina%22"

def run_server():

    data = get_data()

    total = data[0]["total"]

    filtered = filter(filter_none, data[1])

    print(filtered, data[1][0]["value"])


def get_data():
    response = requests.get(API_URL)

    if response.status_code != 200:
        print("Failed fetching data from API", response)

    data = response.json()

    return data

def filter_country(country_data):
    return country_data["country"]["value"] == "Argentina" 

    
if __name__ == "__main__":
    run_server()
   
