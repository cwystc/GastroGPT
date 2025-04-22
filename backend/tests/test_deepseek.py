from services import deepseek_service

bot = deepseek_service.DeepSeekChatBot()

print(bot.send_message("Could you help me to recommend a newyork restaurant?"))
print(bot.send_message("Are there any cheap and delicious buffets?"))