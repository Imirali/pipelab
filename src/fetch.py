import requests
import json
from loguru import logger

BASE_URL = "https://hacker-news.firebaseio.com/v0/"

TOP_STORIES_ENDPOINT = "topstories.json"

ITEM_ENDPOINT = "item/{item_id}.json"

def get_query(base_url:str, endpoint:str, timeout:int = 10,item_id:int = None)->dict|list:
    """Get the JSON response from the Hacker News API.

    Args:
        endpoint (str): The endpoint path, e.g. ``topstories.json`` or
            ``item/<id>.json``.

    Returns:
        dict: The parsed JSON response.
    """
    if item_id is not None:
        url = base_url + endpoint.format(item_id=item_id)
    else:
        url = base_url + endpoint

    try:
        response = requests.get(url, timeout=timeout)
        logger.info(f"response status {response.status_code}")
        response.raise_for_status
    except requests.RequestException as e:
        logger.error(f"Request error {e}")
    except requests.ConnectionError as e:
        logger.error(f"Connection error {e}")
    else:
        data = response.json()

    return data


def main():

    responce_top_stories_ids = get_query(BASE_URL, TOP_STORIES_ENDPOINT,10)

    first_1o_ids_stories = responce_top_stories_ids[:10]

    titles = []

    for id in first_1o_ids_stories:
        story= get_query(BASE_URL, ITEM_ENDPOINT,10,id)
        title = story.get("title","untitled")
        titles.append(title)
    
    print(titles)


if __name__ =="__main__":
    main()

