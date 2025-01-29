from flask import Blueprint, render_template
import random, json
from module2 import NRomano

train = Blueprint("train", __name__)

@train.route("/practicar")
def practicar():
	listaÁcidos = []
	listaSales = []
	listaSalesBin = []
	listaÓxidos = []
	listaHidruros = []
	listaHidróxidos = []
	for i in range(10):
		with open('tabla.json', 'r') as f:
			data = json.load(f)
		símboloÁcido = random.choice(data["lista"])
		nombreÁcido = data["elementos"][símboloÁcido]
		fulls = []
		for x in data["ácidos"]:
			if símboloÁcido in data["ácidos"][x]:
				fulls.append(x)
		full = random.choice(fulls)
		#valencia = data["ácidos"][full][símboloÁcido]
		if full == "hipo-oso":
			pref = "hipo"
			suf = "oso"
		elif full == "-oso":
			pref = ""
			suf = "oso"
		elif full == "-ico":
			pref = ""
			suf = "ico"
		elif full == "per-ico":
			pref = "per"
			suf = "ico"
		abrv = data["abreviado"][nombreÁcido]
		if abrv == "fosf":
			abrv = "fosfor"
		if suf == "ico":
			if abrv == "arseni":
				abrv = "arsen"
			elif abrv == "seleni":
				abrv = "selen"
			elif abrv == "antimoni":
				abrv == "antimon"
		if símboloÁcido in data["especiales"]:
			listaEspecial = ["Meta", "Piro", ""]
			prefEspecial = random.choice(listaEspecial)
		else:
			prefEspecial = ""
		if pref == "hipo":
			if abrv == "oxigen":
				abrv = "xigen"
		if pref == "" and prefEspecial == "Meta":
			if abrv == "antimoni":
				abrv = "ntimoni"
			elif abrv == "arseni":
				abrv = "rseni"
		if pref == "" and prefEspecial == "":
			abrv = abrv.capitalize()
		elif prefEspecial == "":
			pref = pref.capitalize()
		listaÁcidos.append(f"Ácido {prefEspecial}{pref}{abrv}{suf}")

		# SALES OXISALES

		símboloSalO = random.choice(data["lista"])
		nombreSalO = data["elementos"][símboloSalO]
		fulls = []
		for x in data["sales"]:
			if símboloSalO in data["sales"][x]:
				fulls.append(x)
		full = random.choice(fulls)
		#valencia = data["sales"][full][símboloSalO]
		if full == "hipo-ito":
			pref = "hipo"
			suf = "ito"
		elif full == "-ito":
			pref = ""
			suf = "ito"
		elif full == "-ato":
			pref = ""
			suf = "ato"
		elif full == "per-ato":
			pref = "per"
			suf = "ato"
		abrv = data["abreviado"][nombreSalO]
		#if abrv == "fosf":
		#	abrv = "fosfor"
		if suf == "ito":
			if abrv == "arseni":
				abrv = "arsen"
			elif abrv == "seleni":
				abrv = "selen"
			elif abrv == "antimoni":
				abrv == "antimon"
		if símboloSalO in data["especiales"]:
			listaEspecial = ["Meta", "Piro", ""]
			prefEspecial = random.choice(listaEspecial)
		else:
			prefEspecial = ""
		if pref == "hipo":
			if abrv == "oxigen":
				abrv = "xigen"
		if pref == "" and prefEspecial == "Meta":
			if abrv == "antimoni":
				abrv = "ntimoni"
			elif abrv == "arseni":
				abrv = "rseni"
		if pref == "" and prefEspecial == "":
			abrv = abrv.capitalize()
		elif prefEspecial == "":
			pref = pref.capitalize()
			

		while True:
			elemento = random.choice(data["todos"])
			if not elemento == símboloSalO:
				break
			
		if elemento in data["valencias"]:
			nombreElemento = data["valencias"][elemento]["nombre"]
			forma = ""
		else:
			nombreElemento = data["valencias2"][elemento]["nombre"]
			val = data["valencias2"][elemento]["valencia"]
			forma = random.choice(val)
			forma = "("+NRomano(int(forma))+")"
		listaSales.append(f"{prefEspecial}{pref}{abrv}{suf} de {nombreElemento} {forma}")
		
		# Sales binarias
		#while True:
		#	elemento = random.choice(data["todos"])
		#	if elemento in data["valencias"] and elemento in data["abreviado"]:
		#		elemento = data["elementos"][elemento]
		#		break
		elemento = random.choice(data["listaAbrv"])
		abrv = data["abreviado"][elemento]
		elemento = random.choice(data["todos"])
		if elemento in data["valencias"]:
			nombreElemento = data["valencias"][elemento]["nombre"]
			forma = ""
		else:
			nombreElemento = data["valencias2"][elemento]["nombre"]
			val = data["valencias2"][elemento]["valencia"]
			forma = random.choice(val)
			forma = "("+NRomano(int(forma))+")"
		if abrv == "sulfur":
			abrv = "sulf"
		listaSalesBin.append(f"{abrv.capitalize()}uro de {nombreElemento} {forma}")

		# Óxidos
		elemento = random.choice(data["todos"])
		if elemento in data["valencias"]:
			nombreElemento = data["valencias"][elemento]["nombre"]
			forma = ""
		else:
			nombreElemento = data["valencias2"][elemento]["nombre"]
			val = data["valencias2"][elemento]["valencia"]
			forma = random.choice(val)
			forma = "("+NRomano(int(forma))+")"
		
		listaÓxidos.append(f"Óxido de {nombreElemento} {forma}")

		# Hidruros
		elemento = random.choice(data["todos"])
		if elemento in data["valencias"]:
			nombreElemento = data["valencias"][elemento]["nombre"]
			forma = ""
		else:
			nombreElemento = data["valencias2"][elemento]["nombre"]
			val = data["valencias2"][elemento]["valencia"]
			forma = random.choice(val)
			forma = "("+NRomano(int(forma))+")"
		listaHidruros.append(f"Hidruro de {nombreElemento} {forma}")

		# Hidróxidos
		elemento = random.choice(data["todos"])
		if elemento in data["valencias"]:
			nombreElemento = data["valencias"][elemento]["nombre"]
			forma = ""
		else:
			nombreElemento = data["valencias2"][elemento]["nombre"]
			val = data["valencias2"][elemento]["valencia"]
			forma = random.choice(val)
			forma = "("+NRomano(int(forma))+")"
		listaHidróxidos.append(f"Hidróxido de {nombreElemento} {forma}")

		
	#print (listaÁcidos)
	#print (listaSalesBin)
	return render_template("train/generar.html",Ácidos=listaÁcidos, Sales=listaSales, SalesBin=listaSalesBin, Óxidos=listaÓxidos, Hidruros=listaHidruros, Hidróxidos=listaHidróxidos)



@train.route("/generar")
def generar():
	# Generar ácido
	with open('tabla.json', 'r') as f:
		data = json.load(f)
	símboloÁcido = random.choice(data["lista"])
	nombreÁcido = data["elementos"][símboloÁcido]
	fulls = []
	for x in data["ácidos"]:
		if símboloÁcido in data["ácidos"][x]:
			fulls.append(x)
	#print (fulls)
	full = random.choice(fulls)
	#valencia = data["ácidos"][full][símboloÁcido]
	if full == "hipo-oso":
		pref = "hipo"
		suf = "oso"
	elif full == "-oso":
		pref = ""
		suf = "oso"
	elif full == "-ico":
		pref = ""
		suf = "ico"
	elif full == "per-ico":
		pref = "per"
		suf = "ico"
	abrv = data["abreviado"][nombreÁcido]
	if abrv == "fosf":
		abrv = "fosfor"
	elif suf == "ico":
		if abrv == "arseni":
			abrv = "arsen"
		elif abrv == "seleni":
			abrv = "selen"
		elif abrv == "antimoni":
			abrv == "antimon"
	if símboloÁcido in data["especiales"]:
		listaEspecial = ["Meta", "Piro", ""]
		prefEspecial = random.choice(listaEspecial)
	else:
		prefEspecial = ""

	if pref == "":
		abrv = abrv.capitalize()
	elif prefEspecial == "":
		pref = pref.capitalize()

	return f"Ácido {prefEspecial}{pref}{abrv}{suf}"
