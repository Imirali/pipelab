import requests
import json
from loguru import logger

BASE_URL = "https://hacker-news.firebaseio.com/v0/"

TOP_STORIES_ENDPOINT = "topstories.json"

ITEM_ENDPOINT = "item/{item_id}.json"

COUNT_ID = 10

def build_url_top_stories(base_url:str, endpoint:str)->str:
    """ Concatenate the base URL with an endpoint to build a full request URL.
    """
    return base_url + endpoint


def build_url_details_by_id(base_url:str, endpoint:str, item_id:int)->str:
    """ Concatenate the details URL with an endpoint to build a full request URL.
    """
    return base_url +endpoint.format(item_id=item_id)

def get_query(url:str, timeout:int = 10)->dict|list:
    """Get the JSON response from the Hacker News API.

    Args:
        endpoint (str): The endpoint path, e.g. ``topstories.json`` or
            ``item/<id>.json``.

    Returns:
        dict: The parsed JSON response.
    """

    try:
        response = requests.get(url, timeout=timeout)
        logger.info(f"response status {response.status_code}")
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Request error {e}")
        return []
    else:
        data = response.json()

    return data

def get_details_by_id(stories_ids:list[int])->list[dict]:
    """

    Args:
        id_list (list[int]): _description_

    Returns:
        dict: _description_
    """
    stories = []
    for story_id in stories_ids:
        url = build_url_details_by_id(BASE_URL,ITEM_ENDPOINT,story_id)
        story = get_query(url,10)
        if not story:
            continue
        stories.append(story)

    return stories

def get_titles(stories:list[dict])->list:
    """_summary_

    Args:
        stories (lict[dict]): _description_

    Returns:
        list: _description_
    """
    titles = []
    for story in stories:
        titles.append(story.get("title","untitled"))

    return titles


def main():

    responce_top_stories_ids = get_query(build_url_top_stories(BASE_URL,TOP_STORIES_ENDPOINT))

    ids_stories = responce_top_stories_ids[:COUNT_ID]

    stories = get_details_by_id(ids_stories)

    titles = get_titles(stories)

    for num, title in enumerate(titles, 1):
        print(f"{num}: {title}")

if __name__ =="__main__":
    main()

