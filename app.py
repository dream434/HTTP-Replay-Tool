import json
from flask import Flask, render_template, request
import requests
import io

app = Flask(__name__)
app.jinja_env.filters['fromjson'] = json.loads

# --- Fonctions utilitaires ---

def load_requests_from_file(filename='requests.json'):
    """
    Charge les requêtes HTTP depuis un fichier JSON.
    """
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erreur: Le fichier '{filename}' n'a pas été trouvé.")
        return []
    except json.JSONDecodeError:
        print(f"Erreur: Le fichier '{filename}' n'est pas un JSON valide.")
        return []

def process_request_form(form_data, files_data):
    """
    Traite les données du formulaire POST et les données des fichiers.
    """
    headers_dict = {}
    header_keys = form_data.getlist('header_key[]')
    header_values = form_data.getlist('header_value[]')

    for key, value in zip(header_keys, header_values):
        if key.strip():
            headers_dict[key.strip()] = value.strip()

    req_data = {
        'method': form_data.get('method'),
        'url': form_data.get('url'),
        'headers': headers_dict,
        'content': form_data.get('content'),
        'protocol': form_data.get('protocol', 'HTTP/1.1'),
    }
    
    # Gère le fichier téléversé si présent
    if 'file_upload' in files_data:
        file_to_upload = files_data['file_upload']
        if file_to_upload.filename != '':
            req_data['file_upload_object'] = file_to_upload

    return req_data

def execute_http_request(req_data):
    """
    Exécute la requête HTTP en utilisant la bibliothèque requests.
    """
    method = req_data['method']
    url = req_data['url']
    headers = req_data['headers']
    timeout = 10
    allow_redirects = False
    
    # Prépare le dictionnaire pour la requête
    request_params = {
        'method': method,
        'url': url,
        'headers': headers,
        'timeout': timeout,
        'allow_redirects' : allow_redirects
    }

    files_payload = None
    data_payload = None

    if 'file_upload_object' in req_data and req_data['file_upload_object']:
        file_upload_obj = req_data['file_upload_object']
        
        # Le nom de champ de fichier attendu par le serveur
        file_field_name = 'file'

        # Prépare le dictionnaire de fichiers pour requests
        files_payload = {
            file_field_name: (file_upload_obj.filename, file_upload_obj.stream, file_upload_obj.mimetype)
        }
        
        request_params['files'] = files_payload
        
        # Requests gère automatiquement le Content-Type
        if 'Content-Type' in request_params['headers']:
            del request_params['headers']['Content-Type']
    elif req_data.get('content') and req_data['content'].strip() != '':
        data_payload = req_data['content']
        request_params['data'] = data_payload


    try:
        # Exécute la requête avec la bibliothèque requests
        resp = requests.request(**request_params)
        return resp
    except requests.exceptions.RequestException as e:
        return f"Une erreur est survenue lors de la requête: {e}"
    except Exception as e:
        return f"Une erreur inattendue est survenue: {e}"

def format_response_output(req_data, resp):
    """
    Formate la réponse HTTP (statut, en-têtes, corps) pour l'affichage.
    """
    output = f"Replayed {req_data['method']} {req_data['url']} with {req_data['protocol']} - Status: {resp.status_code}\n"
    output += "--- Response Headers ---\n"
    for key, value in resp.headers.items():
        output += f"{key}: {value}\n"
    output += "--- Response Body ---\n"
    output += resp.text
    return output

@app.route('/', methods=['GET', 'POST'])
def index():
    requests_data = load_requests_from_file()
    output_result = None

    if request.method == 'POST':
        req_to_replay = process_request_form(request.form, request.files)
        response_or_error = execute_http_request(req_to_replay)

        if isinstance(response_or_error, requests.Response):
            output_result = format_response_output(req_to_replay, response_or_error)
        else:
            output_result = response_or_error

    return render_template('index.html', requests=requests_data, output=output_result)

if __name__ == '__main__':
    app.run(debug=True)