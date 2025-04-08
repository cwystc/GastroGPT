from utils import text_processing
from api import rag

from models import embedding_model

from services import deepseek_service

def answer_to_user(question, index, indexid_to_restaurant):
    cleaned_question = text_processing.clean_text(question)


    # step 1
    distances, indices = rag.search_restaurants(index, cleaned_question, k=30)

    # 6. Get the restaurant information


    top10_restaurants = []
    for indexid in indices[0]:
        if (indexid == -1):
            break
        if any(obj is indexid_to_restaurant[indexid] for obj in top10_restaurants):
            continue
        top10_restaurants.append(indexid_to_restaurant[indexid])
        if (len(top10_restaurants) >= 10):
            break

    # for restaurant in top10_restaurants:
    #     print(restaurant.info)
    
    bot = deepseek_service.DeepSeekChatBot()

    construct_prompt = "Your task is to pick one resturant to recommend to the users. I will give you the information of the restaurants and user's request. The information of the restaurants are as follows: "

    for restaurant in top10_restaurants:
        construct_prompt += restaurant.info+"\n"
    
    construct_prompt += "The user's request is as follows: " + question

    
    ans = bot.send_message(construct_prompt)
    return ans