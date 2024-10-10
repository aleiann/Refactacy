from flask import Blueprint, redirect, request, session, url_for, render_template_string, jsonify
import requests
from utils.gitUtils import extract_owner_and_repo, get_repo_structure, get_file_content
import os
from dotenv import load_dotenv

githubService = Blueprint('gitService', __name__)

# Carica le variabili dall'.env
load_dotenv()

# Recupera le credenziali
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
GITHUB_ACCESS_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_API_URL = "https://api.github.com"

@githubService.after_request
def add_cors_headers(response):
    # Aggiungi l'intestazione Access-Control-Allow-Origin per permettere tutte le origini
    response.headers['Access-Control-Allow-Origin'] = '*'
    # Se necessario, puoi anche aggiungere altri headers CORS
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

# Pagina per inserire l'URL del repository
@githubService.route('/')
def index():
    form_html = '''
        <h2>Autorizza l'accesso a un repository specifico</h2>
        <form action="/authorize_repo" method="POST">
            <label for="repo_url">Inserisci l'URL del repository:</label>
            <input type="text" id="repo_url" name="repo_url" placeholder="https://github.com/owner/repo" required>
            <button type="submit">Autorizza</button>
        </form>
    '''
    return render_template_string(form_html)

# Autorizza il repository specificato dall'utente
@githubService.route('/authorize_repo', methods=['POST'])
def authorize_repo():
    repo_url = request.form.get('repo_url')
    owner, repo = extract_owner_and_repo(repo_url)

    if owner and repo:
        # Memorizza il repository nella sessione
        session['owner'] = owner
        session['repo'] = repo

        # Richiede autorizzazione con scope per i repository
        github_auth_url = f"{GITHUB_AUTHORIZE_URL}?client_id={CLIENT_ID}&scope=repo"
        return redirect(github_auth_url)
    else:
        return "URL non valido", 400

@githubService.route('/callback')
def callback():
    return redirect('http://127.0.0.1:5000/view_file')


# Visualizza il contenuto di un file
@githubService.route('/view_file')
def view_file():
    access_token = session.get('access_token')
    owner = session.get('owner')
    repo = session.get('repo')
    file_path = request.args.get('path')

    if not access_token or not owner or not repo or not file_path:
        return redirect(url_for('index'))

    # Recupera il contenuto del file
    file_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    file_content = get_file_content(file_url, access_token=access_token)

    if file_content:
        return f"<h2>Contenuto del file: {file_path}</h2><pre>{file_content}</pre>"
    else:
        return "Errore nel recupero del contenuto del file", 400