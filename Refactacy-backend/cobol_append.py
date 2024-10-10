import base64
import requests
import re


# Funzione per recuperare il contenuto del file principale
def get_github_file_content(owner, repo, path):

    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(url)

    if response.status_code == 200:
        content = response.json()
        # Il contenuto del file è codificato in base64, quindi dobbiamo decodificarlo
        file_content = base64.b64decode(content['content']).decode('utf-8')
        return file_content
    else:
        print(f"Errore nel recupero del file {path}: {response.status_code}")

#Funzione per cercare le istruzioni "COPY" e "CALL"
def find_copy_and_call_statements(file_content):
    copy_statements = re.findall(r'COPY\s+"([^"]+)\.CPY"', file_content)
    call_statements = re.findall(r'CALL\s+["\'](\S+)["\']', file_content)
    return copy_statements, call_statements

#Funzione che ritorna il codice completo
def get_full_cobol_code(owner, repo, path, processed_files = None):
    if processed_files is None:
        processed_files = set()  # Set per tenere traccia dei file già processati e evitare loop
    if path in processed_files:
        return ""  # Evita di processare lo stesso file più volte
    processed_files.add(path)

    file_content = get_github_file_content(owner, repo, path)
    if not file_content:
        return ""
    full_code = file_content

    # Cerca le istruzioni COPY e CALL
    copy_statements, call_statements = find_copy_and_call_statements(file_content)

    # Recupero e concatenazione dei file richiamati dalle istruzioni COPY
    for copy_file in copy_statements:
        # Normalizza il nome del file (rimuove spazi e aggiunge .cpy)
        copy_file_path_upper = copy_file.strip().upper() + '.cpy'
        copy_file_path_lower = copy_file.strip().lower() + '.cpy'

        # Prova prima con il percorso maiuscolo
        copy_content = get_full_cobol_code(owner, repo, copy_file_path_upper, processed_files)

        if not copy_content:
            # Se non trova il file maiuscolo, prova con il percorso minuscolo
            copy_content = get_full_cobol_code(owner, repo, copy_file_path_lower, processed_files)

        if copy_content:
            full_code += f"\n* COPY {copy_file}\n" + copy_content

    # Recupero e concatenazione dei file richiamati dalle istruzioni CALL
    for call_file in call_statements:
        call_file_path_upper = call_file.strip().upper() + '.cbl'
        call_file_path_lower = call_file.strip().lower() + '.cbl'

        call_content = get_full_cobol_code(owner, repo, call_file_path_upper, processed_files)
        if not call_content:
            # Se non trova il file maiuscolo, prova con il percorso minuscolo
            call_content = get_full_cobol_code(owner, repo, call_file_path_lower, processed_files)

        if call_content:
            full_code += f"\n* CALL {call_file}\n" + call_content

    return full_code

# Concatena il contenuto di tutti i file .dat all'interno della repo
def get_dat_content(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/"
    response = requests.get(url)

    if response.status_code == 200:
        files = response.json()
        dat_files_content = []

        # Loop su tutti i file per filtrare i .dat
        for file in files:
            if file['name'].endswith('.dat'):
                file_url = file['download_url']

                # Recupera il contenuto del file
                file_content_response = requests.get(file_url)

                if file_content_response.status_code == 200:
                    # Decodifica il contenuto (se è base64)
                    content = file['name'] + "\n" + file_content_response.text + "\n"
                    dat_files_content.append(content)
                else:
                    print(f"Errore nel recuperare {file['name']}: {file_content_response.status_code}")

        # Concatenazione di tutti i file .dat
        concatenated_content = "\n".join(dat_files_content)
        return concatenated_content
    else:
        print(f"Errore nel recupero del file : {response.status_code}")
