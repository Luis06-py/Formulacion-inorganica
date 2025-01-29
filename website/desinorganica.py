from flask import Blueprint, render_template, redirect, session, request
import json
from module2 import NRomano
# Error 9 -> No se puede hacer la inversa
def getvalencia(elemento):
	with open('tabla.json', 'r') as f:
		data = json.load(f)
	return data["valencias"][elemento]["valencia"]

desinorganica = Blueprint("desinorganica", __name__)

@desinorganica.route("/inversa", methods=["POST"])
def inversa():
	try:
		fórmula = request.form["fórmula"]
	except:
		return render_template('405.html')
	if fórmula == "":
		render_template("error.html", code=1, descripción="No se han rellenado todos los datos")
	return ("Fórmula "+fórmula)