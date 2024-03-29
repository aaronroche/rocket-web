import requests
from bs4 import BeautifulSoup
import json

url = 'https://nextspaceflight.com/launches/'
results = []


def webscrape(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    launches = soup.find_all('div', class_='launch')

    for launch in launches:
        title = launch.find('h5', class_='header-style').text.split('|')
        name = title[0].strip()
        payload = title[1].strip()
        company = launch.find('span')
        details = launch.find('div', class_='mdl-card__supporting-text')

        results.append({"name": name,
                        "payload": payload,
                        "company": company.text.strip(),
                        "details": [item.strip() for item in details.text.strip().split('\n') if item.strip()]})

    json_output = json.dumps(results)
    print(json_output)

    return


webscrape(url)
