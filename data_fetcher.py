#  -*- coding: utf-8 -*-
#  @filename data_fetcher.py
#  @author Marcel Bobolz
#  @last_modified 2025-03-14T13:30:27.135Z
"""Retrieve data from api-ninjas.com"""

import requests

from dotenv import load_dotenv
from sys import exit
from typing import Any, Dict, List
from os import environ

NINJAS_API_URL = "https://api.api-ninjas.com/v1/animals?name={}"


def require_dotenv(func):
    """Decorator that retrieves the api-key from file"""

    def wrap(*args, **kwargs):
        load_dotenv()
        return func(*args, **kwargs)

    return wrap


@require_dotenv
def fetch_data(animal_name: str = "Fox") -> List[Dict[str, Any]]:
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
    api_key = environ.get("API_KEY")
    if not api_key:
        print("""Please set the value for environment variable 'API_KEY' first !
      (either export or set in .env-file)""")
        exit(1)

    response = requests.get(NINJAS_API_URL.format(animal_name), headers={"X-Api-Key": api_key}, timeout=5)
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        raise requests.RequestException(f"Error: [{response.status_code}] {response.text}")


if __name__ == "__main__":
    data = fetch_data()
    print(data[1])
