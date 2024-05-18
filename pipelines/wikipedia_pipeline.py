import json
import time
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError


NO_IMAGE = 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/No-image-available.png/480px-No-image-available.png'


def get_wikipedia_page(url):
    import requests

    print("Getting wikipedia page...", url)

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # check if the request is successful

        return response.text
    except requests.RequestException as e:
        print(f"An error occured: {e}")

def get_wikipedia_data(html):
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all("table", {"class": "wikitable sortable"})

    table_rows = []
    for table in tables[0:6]:
        table_rows.append(table.find_all('tr'))

    return table_rows

def clean_text(text):
    text = str(text).strip()
    text = text.replace('&nbsp', '')
    if text.find(' ♦'):
        text = text.split(' ♦')[0]
    if text.find('[') != -1:
        text = text.split('[')[0]
    if text.find(' (formerly)') != -1:
        text = text.split(' (formerly)')[0]

    return text.replace('\n', '')

def extract_wikipedia_data(**kwargs):
    url = kwargs['url']
    html = get_wikipedia_page(url)
    rows = get_wikipedia_data(html)

    data = []
    counter = 1
    for row in rows:
        for i in range(1, len(row)):
            tds = row[i].find_all('td')
            values = {
                'rank': counter,
                'stadium': clean_text(tds[0].text),
                'capacity': clean_text(tds[1].text).replace(',', '').replace('.', ''),
                'city': clean_text(tds[2].text),
                'country': clean_text(tds[3].text),
                'home_team': clean_text(tds[4].text),
                'images': 'https://' + tds[5].find('img').get('src').split("//")[1] if len(tds)==6 and tds[5].find('img') else "NO_IMAGE"
                
            }
            counter = counter + 1
            data.append(values)

    json_rows = json.dumps(data)
    kwargs['ti'].xcom_push(key='rows', value=json_rows)

    return "OK"

def get_lat_long(country, city):
    geolocator = Nominatim(user_agent='geoapiExercises')
    
    try:
        location = geolocator.geocode(f'{city}, {country}')
        if location:
            return location.latitude, location.longitude
    except GeocoderServiceError as e:
        print(f"Geocoding service error: {e}")
        # Optionally, you can wait for some time before retrying
        time.sleep(1)  # Sleep for 1 second before retrying
        # You can also handle other errors or raise an exception if needed
        # raise

    return None

def transform_wikipedia_data(**kwargs):
    data = kwargs['ti'].xcom_pull(key='rows', task_ids='extract_data_from_wikipedia')

    data = json.loads(data)

    stadiums_df = pd.DataFrame(data)
    stadiums_df['location'] = stadiums_df.apply(lambda x: get_lat_long(x['country'], x['stadium']), axis=1)
    stadiums_df['images'] = stadiums_df['images'].apply(lambda x: x if x not in ['NO_IMAGE', '', None] else NO_IMAGE)
    stadiums_df['capacity'] = stadiums_df['capacity'].astype(int)

    # handle the duplicates
    duplicates = stadiums_df[stadiums_df.duplicated(['location'])]
    duplicates['location'] = duplicates.apply(lambda x: get_lat_long(x['country'], x['city']), axis=1)
    stadiums_df.update(duplicates)

    # push to xcom
    kwargs['ti'].xcom_push(key='rows', value=stadiums_df.to_json())

    return "OK"

def write_wikipedia_data(**kwargs):
    from datetime import datetime
    data = kwargs['ti'].xcom_pull(key='rows', task_ids='transform_wikipedia_data')

    data = json.loads(data)
    data = pd.DataFrame(data)

    file_name = ('stadium_cleaned_' + str(datetime.now().date())
                 + "_" + str(datetime.now().time()).replace(":", "_") + '.csv')

    # data.to_csv('data/' + file_name, index=False)
    data.to_csv('abfs://cricketdataeng@cricketdataeng.dfs.core.windows.net/data/' + file_name,
                storage_options={
                    'account_key': 'xxxxxxxxxxxxxx'
                }, index=False)

