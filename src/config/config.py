from dotenv import load_dotenv
import os

load_dotenv()

APP_NAME="Chatbot ABY"
URL_API="https://estudio-juridico-camacho-gomez.pockethost.io/api"
URL_API_WS = "https://api.ultramsg.com/"
API_KEY_GROQ=os.getenv("API_KEY_GROQ")
USE_AI=os.getenv("USE_AI", False)

print(type(USE_AI))

global bot_step
bot_step = 1
# python -m spacy download es_core_news_sm