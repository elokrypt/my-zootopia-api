"""Retrieve data from api-ninjas.com"""

import requests

from dotenv import load_dotenv
from os import getenv

global API_KEY
NINJAS_API_ANIMALS_URL = "https://api.api-ninjas.com/v1/animals?name={}"


def require_api_key(func):
    """Decorator that retrieves the api-key from file"""

    def wrap(*args, **kwargs):
        global API_KEY
        load_dotenv()
        API_KEY = getenv("API_KEY")
        return func(*args, **kwargs)

    return wrap


@require_api_key
def fetch_data(animal_name: str = "Fox") -> [dict, ...]:
    """
    Fetches the animals data for the animal 'animal_name'.
    Returns: a list of animals, each animal is a dictionary:
    {
      'name': ...,
      'taxonomy': {
        ...
      },
      'locations': [
        ...
      ],
      'characteristics': {
        ...
      }
    },"""
    global API_KEY
    response = requests.get(NINJAS_API_ANIMALS_URL.format(animal_name), headers={"X-Api-Key": API_KEY})
    if response.status_code == requests.codes.ok:
        retval: [] = response.json()
        if len(retval) > 1:
            return retval
        else:
            retval.insert(0, {"invalid_name": animal_name})
            return retval
    else:
        raise requests.RequestException(f"Error: [{response.status_code}] {response.text}")
