from feature.chatbot.api.ws_api import UltraMsgAPI
from dotenv import load_dotenv
import os

load_dotenv()

class MessageActions:
    def __init__(self):
        INSTANCE_ID = os.getenv("INSTANCE_ID")
        API_TOKEN = os.getenv("API_TOKEN")
        self.ultramsg_api = UltraMsgAPI(INSTANCE_ID, API_TOKEN)

    def send_simple_message(self, to, message):
        """Envía un mensaje simple."""
        return self.ultramsg_api.send_message(to, message)

    def send_personalized_message(self, to, name, template):
        """Envía un mensaje personalizado utilizando un template."""
        personalized_message = template.replace("{name}", name)
        return self.ultramsg_api.send_message(to, personalized_message)
