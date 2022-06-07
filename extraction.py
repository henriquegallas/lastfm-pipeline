from dotenv import load_dotenv
import os
import requests
import json
import csv


load_dotenv()

# getting environment variables from .env file
api_key = os.environ.get('API_KEY')
user_agent = os.environ.get('USER_AGENT')


def get_top_artists(user, period):
    # define headers and url
    headers = {'user-agent': user_agent}
    url = 'https://ws.audioscrobbler.com/2.0/'

    # define parameters dict
    params = {
        'api_key': api_key,
        'format': 'json',
        'method': 'user.gettopartists',
        'limit': 100,
        'user': user,
        'period': period
    }

    response = requests.get(url, headers=headers, params=params)
    return response


def parse_top_artists_json_to_csv(response_content):
    # create a json object from the response content
    response_json = json.loads(response_content)

    all_passes = []

    for artist in response_json['topartists']['artist']:
        current_pass = []

        # store the rank, name and playcount of the pass
        current_pass.append(artist['@attr']['rank'])
        current_pass.append(artist['name'])
        current_pass.append(artist['playcount'])

        all_passes.append(current_pass)

    export_file = 'export_file.csv'

    try:
        # create the csv file
        with open(export_file, 'w') as fp:
            csvw = csv.writer(fp, delimiter=',')
            csvw.writerows(all_passes)
        
        fp.close()
        print('Top Artists csv file successfully created.')
    except:
        print('Error while creating csv file.')


user = 'ique26'
period = 'overall'

r = get_top_artists(user, period)
response_content = r.content
parse_top_artists_json_to_csv(response_content)
