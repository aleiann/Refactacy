import base64
import requests
import re



def remove_git_extension(repo_url):
    if repo_url.endswith('.git'):
        return repo_url[:-4]  # Rimuove gli ultimi 4 caratteri ".git"
    return repo_url

# Funzione per estrarre il proprietario e il nome del repository dall'URL
def extract_owner_and_repo(repo_url):
    try:
        parts = repo_url.strip().split('/')
        owner = parts[-2]
        repo = remove_git_extension(parts[-1])
        return owner, repo
    except IndexError:
        return None, None

# Funzione per recuperare la struttura del repository
def get_repo_structure(owner, repo, path="", access_token=None):
    headers = {
        'Authorization': f'token {access_token}' if access_token else None
    }

    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(url, headers=headers)

    # Controllo della risposta
    if response.status_code == 200:
        contents = response.json()
        structure = []

        # Aggiungere file e cartelle alla struttura
        files = []
        for item in contents:
            if item['type'] == 'file':
                files.append(item['path'])  # Aggiungi il file alla lista dei file
            elif item['type'] == 'dir':
                # Se è una directory, chiama ricorsivamente la funzione
                sub_structure = get_repo_structure(owner, repo, item['path'], access_token)
                # Aggiungere la cartella e i suoi file
                structure.append({
                    'folder': item['path'],
                    'files': []  # Inizializza con una lista vuota
                })
                # Aggiungere i file trovati nelle sottocartelle
                for sub_item in sub_structure:
                    if isinstance(sub_item, dict):
                        structure[-1]['files'].extend(sub_item['files'])  # Estendi i file della sottocartella

        # Aggiungere i file della cartella corrente alla struttura
        if path:  # Evita di creare una cartella radice
            structure.append({
                'folder': path,
                'files': files
            })
        else:  # Se siamo nella radice, aggiungiamo i file direttamente
            structure.append({
                'folder': '/',
                'files': files
            })
        return structure
    else:
        print(f"Errore nella richiesta: {response.status_code} - {response.text}")
        return []

# Funzione per recuperare il contenuto del file
def get_file_content(file_url, access_token=None):
    headers = {
        'Authorization': f'token {access_token}' if access_token else None
    }

    response = requests.get(file_url, headers=headers)

    if response.status_code == 200:
        file_info = response.json()
        if file_info['encoding'] == 'base64':
            content = base64.b64decode(file_info['content']).decode('utf-8')
            return content
        else:
            return None
    else:
        return None