from flask import Blueprint, request
import os
from dotenv import load_dotenv
from llm import interagisci_con_gpt4

openAiService = Blueprint('openAiService', __name__)

# Carica le variabili dall'.env
load_dotenv()
# Recupera le credenziali
API_KEY = os.getenv('API_KEY')
PROJECT_KEY = os.getenv('PROJECT_KEY')

@openAiService.route('/openai')
def index():
    name = request.args.get('name')
    prompt = 'rispondimi solo con il nome del linguaggio di programmazione di un file chiamato ' + name
    res = interagisci_con_gpt4(API_KEY, PROJECT_KEY, prompt)
    return res


