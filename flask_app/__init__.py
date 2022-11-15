from flask import Flask
from flask_awscognito import AWSCognitoAuthentication
app = Flask(__name__)

app.secret_key = "The hate keeps me warm"

