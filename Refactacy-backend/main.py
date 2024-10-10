from flask import Flask
from service.gitService import githubService
from service.openAiService import openAiService
from service.cobolService import cobolService
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will allow all domains to access your API
app.secret_key = os.urandom(24)

app.register_blueprint(githubService)
app.register_blueprint(openAiService)
app.register_blueprint(cobolService)

if __name__ == "__main__":
    app.run(debug=True)
