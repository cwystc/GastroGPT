from utils import text_processing
from api import rag

from models import embedding_model

from services import deepseek_service
import json

def clean_markdown_json(response_text):
    lines = response_text.strip().splitlines()
    json_lines = [line for line in lines if not line.strip().startswith("```")]
    return "\n".join(json_lines)

def answer_to_user(question, index, indexid_to_restaurant):
    cleaned_question = text_processing.clean_text(question)


    # step 1
    distances, indices = rag.search_restaurants(index, cleaned_question, k=60)

    # 6. Get the restaurant information


    top10_restaurants = []
    for indexid in indices[0]:
        if (indexid == -1):
            break
        if any(obj is indexid_to_restaurant[indexid] for obj in top10_restaurants):
            continue
        top10_restaurants.append(indexid_to_restaurant[indexid])
        if (len(top10_restaurants) >= 30):
            break

    # for restaurant in top10_restaurants:
    #     print(restaurant.info)
    
    bot = deepseek_service.DeepSeekChatBot()

    construct_prompt = "Your task is to pick top 3 resturants to recommend to the users. I will give you the information of the restaurants and user's request. The information of the restaurants are as follows: "

    for restaurant in top10_restaurants:
        construct_prompt += restaurant.info+"\n"
    
    construct_prompt += "The user's request is as follows: " + question

    construct_prompt += "For your response, please format the answer as an json as follows."

    construct_prompt += '''
    [
    {
        "name": "Restaurant Name 1",
        "url": "the url of the restaurant.",
        "reason": "One sentence as the reason for recommendation."
    },
    {
        "name": "Restaurant Name 2",
        "url": "the url of the restaurant.",
        "reason": "One sentence as the reason for recommendation."
    },
    {
        "name": "Restaurant Name 3",
        "url": "the url of the restaurant.",
        "reason": "One sentence as the reason for recommendation."
    }
    ]
    '''

    response_text = bot.send_message(construct_prompt)
    cleaned = clean_markdown_json(response_text)

    print(cleaned)

    parsed = json.loads(cleaned)

    return parsed