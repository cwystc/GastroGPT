import function3
import function2

current_location = (33.7756, -84.3963)
index, indexid_to_restaurant = function2.fetch_and_create_index(location=current_location, N = 100)

question = 'I want some korean food with crispy fries'

function3.answer_to_user(question, index, indexid_to_restaurant)