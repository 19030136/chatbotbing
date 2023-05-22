from django.shortcuts import render
from django.http import JsonResponse
from django.urls import path
import asyncio
import re
from EdgeGPT import Chatbot, ConversationStyle
from .models import ChatHistory
from asgiref.sync import sync_to_async

loop = asyncio.get_event_loop()

async def chat_with_bing(user_input):
    bot = Chatbot(cookie_path='bingapp\cookies.json')
    response = await bot.ask(prompt=user_input, conversation_style=ConversationStyle.creative)

    # Extract the bot's response from the conversation
    messages = response.get("item", {}).get("messages", [])
    bot_response = ""

    for message in messages:
        if message.get("author") == "bot":
            bot_response += message.get("text", "") + "\n"

    # Remove any unwanted formatting from the bot's response
    bot_response = re.sub(r'\\[\\^(\d+)\\^]', r'\\1', bot_response)
    bot_response = re.sub(r'\[.*?\]|\*|\^', '', bot_response)
    bot_response = re.sub('```markdown\n+', '', bot_response)
    bot_response = bot_response.strip()

    await bot.close()

    return bot_response


async def chat_view(request):
    if request.method == 'POST':
        try:
            user_input = request.POST['user_input']
            bot_response = await chat_with_bing(user_input)

            await save_chat_history(user_input, bot_response)  # Call save_chat_history asynchronously

          # Add the user input and bot response to the conversation display
            conversation = f"You: {user_input}\nBot: {bot_response}"
            
            return JsonResponse({'response': bot_response})
        except BrokenPipeError:
            # Handle the Broken Pipe error here
            print("Broken pipe error occurred")
            return JsonResponse({'response': ''})
    return render(request, 'chat.html')
@sync_to_async
def save_chat_history(user_input, bot_response):
    chat_history = ChatHistory(user_input=user_input, bot_response=bot_response)
    chat_history.save()


def chat_view_wrapper(request):
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(chat_view(request))
