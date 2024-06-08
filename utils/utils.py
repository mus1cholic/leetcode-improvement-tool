from . import constants as constants

import requests

# TODO: make these api calls resistant to failures/unexpected key types

def api_get_user_info(lc_username):
    return requests.get(f"{constants.API_BASE_LINK}/{lc_username}")

def api_get_question_info(title_slug):
    return requests.get(f"{constants.API_BASE_LINK}/select?titleSlug={title_slug}")

def api_get_user_contest_info(lc_username):
    return requests.get(f"{constants.API_BASE_LINK}/{lc_username}/contest")

def discord_get_attachment_content(url: str):
    file_request = requests.get(url)

    return file_request.content

def convert_topicTags_to_tags_array(topicTags: list):
    return [topic_tag_object["slug"] for topic_tag_object in topicTags]