import requests
import json
import os
import re

root_path = os.path.dirname(os.path.abspath(__file__))

url = 'https://api.vndb.org/kana'
headers = {
    'Content-Type': 'application/json',
}
# Searching for and fetching database entries is done through a custom query format. Queries are sent as POST requests.
# A query is a JSON object that looks like this:
query = {
    "filters": [],  # Filters are used to determine which database items to fetch
    "fields": "",  # String. Comma-separated list of fields to fetch for each database item. Dot notation can be used to select nested JSON objects.
    "sort": "id",  # Field to sort on.
    "reverse": False,  # Set to true to sort in descending order.
    "results": 100,  # Number of results per page, max 100.
    "page": 1,  # Page number to request, starting from 1.
    "user": None,  # User ID. This field is mainly used for POST /ulist.
    "count": False,
    "compact_filters": False,
    "normalized_filters": False
}


def query_vndb(endpoint, filters, fields):
    query['filters'] = filters
    query['fields'] = fields
    response = requests.post(f'{url}/{endpoint}', headers=headers, json=query)
    if response.status_code != 200:
        print(f'Error: {response.status_code}, {response.text}')
        return None
    else:
        return response.json()


# Find the vn_id on the VN's page on VNDB, ex: https://vndb.org/v5154 -> vn_id = v5154
def get_character_data(vn_id):
    character_data = query_vndb('character', ["vn", "=", ["id", "=", vn_id]], "name, description, age, sex, vns.role, traits.name, traits.group_name")
    if character_data is not None:
        valid_characters = []
        # Add only Main and Side characters to the list
        for character in character_data['results']:
            for vn in character['vns']:
                if vn['id'] == vn_id:
                    if vn['role'] != 'appears':
                        # Format before adding
                        valid_characters.append(_format_character(character))
        with open(f'{root_path}/{vn_id}_characters.json', "w", encoding="utf-8") as json_file:
            json.dump(valid_characters, json_file, ensure_ascii=False, indent=4)
        # FOR DEBUGGING
        with open(f'{root_path}/{vn_id}_characters_RAW.json', "w", encoding="utf-8") as json_file:
            json.dump(character_data, json_file, ensure_ascii=False, indent=4)


def get_character_names(vn_id):
    character_data = query_vndb('character', ["vn", "=", ["id", "=", vn_id]], "name, vns.role")
    if character_data is not None:
        character_names = []
        # Add only Main and Side characters to the list
        for character in character_data['results']:
            for vn in character['vns']:
                if vn['id'] == vn_id:
                    if vn['role'] != 'appears':
                        character_names.append(character['name'])
        print(character_names)
        return character_names


def search_vn_title(title):
    vn_data = query_vndb('vn', ["search", "=", title], "id, title")
    if vn_data is not None:
        with open(f'{root_path}/vn_search_results.json', "w", encoding="utf-8") as json_file:
            json.dump(vn_data, json_file, ensure_ascii=False, indent=4)

#
# PRIVATE HELPER FUNCTIONS


def _format_character(char):
    # Format character data
    character = {}
    character['name'] = char['name']
    # Remove all text enclosed in [ ], as well as the credits after \n\n
    character['description'] = re.sub(r'(\[.*?\]|\n\n.*)', '', char['description']).replace('’', "'")
    character['age'] = char['age']
    personality_traits = []
    body_traits = []
    # Possible group names: Personality, Hair, Body, Role, Engages In, 
    for traits in char['traits']:
        if traits['group_name'] == 'Personality':
            personality_traits.append(traits['name'])
        if traits['group_name'] == 'Body':
            body_traits.append(traits['name'])
    character['personality'] = ', '.join(personality_traits)
    character['body'] = ', '.join(body_traits)
    return character

# Testing
# get_character_data('v5154')