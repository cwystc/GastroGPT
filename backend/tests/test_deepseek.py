from services import deepseek_service

bot = deepseek_service.DeepSeekChatBot()

print(bot.send_message("推荐一家纽约的川菜馆"))
print(bot.send_message("有没有便宜又好吃的自助餐？"))