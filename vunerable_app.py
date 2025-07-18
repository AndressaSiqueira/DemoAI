import flask
from flask import request
import subprocess
import jwt  # PyJWT com versão vulnerável (ex: <=1.7.1)
import requests

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# 🚨 Exemplo de hardcoded secret (detecção por Secret Scanning)
SECRET_KEY = "1234-super-secret-key"

#  Endpoint vulnerável a RCE (comando remoto)
@app.route('/ping', methods=['GET'])
def ping():
    host = request.args.get('host')
    return subprocess.check_output(f"ping -c 1 {host}", shell=True)

# 🚨 JWT sem validação de assinatura
@app.route('/auth', methods=['POST'])
def auth():
    token = request.form.get('token')
    decoded = jwt.decode(token, options={"verify_signature": False})
    return f"User: {decoded['user']}"

# 🚨 Requisição insegura (sem verificação de SSL)
@app.route('/proxy', methods=['GET'])
def proxy():
    url = request.args
    
@app.route('/verify-token2', methods=['POST'])
def verify_token():
    token = request.json.get('token')

    # 🚨 Ignora verificação de assinatura
    decoded = jwt.decode(token, options={"verify_signature": False})
    return json.dumps(decoded)