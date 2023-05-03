from telegram.ext import *
import requests
from bs4 import BeautifulSoup

TOKEN = '5726018623:AAH6EAx_N9oYBt-p9pTIMNegnzMMoD2KiMY'
def get_anime_link(anime_name):
  # Send a GET request to the search page with the user's input as the search query
  response = requests.get(f'https://9anime.vc/search?keyword={anime_name}')

  # Check the status code to make sure the request was successful
  if response.status_code != 200:
    raise ValueError('Failed to send request')

  # Parse the HTML of the search page
  soup = BeautifulSoup(response.text, 'html.parser')
  
  # Extract the first result from the search page
  result = soup.find('div', {'class': 'film-poster'})
  # Extract the link from the result
  link = result.find('a').get('href')
  link = 'http://9anime.vc'+link
  return link
def start_command(update, context):
    update.message.reply_text('Hello There! You have started the bot')
def help_command(update, context):
    update.message.reply_text('type /custom to start the bot and then enter the anime of your liking')
def custom_command(update, context):
    update.message.reply_text('Now please enter the anime of your liking')
def handle_response(txt: str)->str:
    return get_anime_link(txt)
def handle_message(update, context):
    message_type = update.message.chat.type
    txt = str(update.message.text)
    response = ''

    print('User ({update.message.chat.id}) says: "{txt} in {message.type}"')
    #if message_type == 'group':
     #   if'https://t.me/PeterRathree_bot' in txt:
    #        response = handle_response(txt.replace('https://t.me/PeterRathree_bot', '').strip())
    #else:
    response = handle_response(txt)
    
    update.message.reply_text('You can watch the anime '+txt+' at '+response)
def error(update,context):
    print(f'Update {update} caused error: {context.error}')
if __name__ == "__main__":
    updater = Updater(TOKEN, use_context=True)
    #Commands
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('custom', custom_command))
    #Messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    #Errors
    dp.add_error_handler(error)
    #Running the Bot

    updater.start_polling(1.0)
    updater.idle()
