import requests
from bs4 import BeautifulSoup
import json

def lambda_handler(event, context):
    url = 'https://nextspaceflight.com/launches/'

    # Parse website then store as JSON object
    results = webscrape(url)

    # Print JSON to console
    print(results)

def webscrape(url):
    results = []
    try:
        # Retrieve website information
        response = requests.get(url, timeout=10)
    except requests.exceptions.ConnectionError as errc:
        print("Error - connection")
    except requests.exceptions.HTTPError as errhttp:
        print("Error - Http")
    except requests.exceptions.Timeout as errt:
        print("Error - timeout")
    except requests.exceptions.TooManyRedirects as errmany:
        print("Error - too many redirects")
    except Exception as e:
        print("An error occurred")
    else:
        # Parse website
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all launches
        launches = soup.find_all('div', class_='launch')

        # Separate by categories
        for launch in launches:
            title = launch.find('h5', class_='header-style').text.split('|')
            name = title[0].strip()
            payload = title[1].strip()
            company = launch.find('span')
            details = launch.find('div', class_='mdl-card__supporting-text')

            # Store characteristics of launch into a list
            results.append({"name": name,
                            "payload": payload,
                            "company": company.text.strip(),
                            "details": [item.strip() for item in details.text.strip().split('\n') if item.strip()]})

        # Convert list to JSON
        json_output = json.dumps(results)
        return json_output
    
    return None     # Exception was caught
