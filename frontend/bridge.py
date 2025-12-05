# bridge.py
from flask import Flask, request, Response
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # permite llamadas desde el navegador

# URL donde corre tu servicio Spyne
SOAP_REAL_URL = "http://localhost:8000/"   # ajusta si tu SOAP corre en otro puerto

@app.route("/alumno", methods=["POST"])
def alumno_bridge():
    headers = {"Content-Type": "text/xml"}
    xml = request.data
    resp = requests.post(SOAP_REAL_URL, data=xml, headers=headers)
    return Response(resp.content, status=resp.status_code, mimetype="text/xml")

if __name__ == "__main__":
    app.run(port=5000)
