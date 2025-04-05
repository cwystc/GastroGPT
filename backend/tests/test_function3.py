import backend.query_llm as query_llm
import backend.fetch_maps_data as fetch_maps_data

current_location = (33.7756, -84.3963)
index, indexid_to_restaurant = fetch_maps_data.fetch_and_create_index(location=current_location, N = 100)

question = 'I want some korean food with crispy fries'

query_llm.answer_to_user(question, index, indexid_to_restaurant)