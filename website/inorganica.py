from flask import Blueprint, render_template, request, redirect, url_for, session
import json
from module2 import NRomano
def errordesc(code):
	if code == 1: # hecho
		return "No se han rellenado todos los datos"
	elif code == 2: # hecho
		return "No se han encontrado esos elementos en la Tabla periódica"
	elif code == 3: # hecho
		return "El elemento no tiene la valencia indicada"
	elif code == 4: # hecho
		return "El elemento debe tener una valencia fija"
	elif code == 5: # hecho
		return "El elemento no puede ser formulado en un Ácido o Sal Oxsial"
	elif code == 6: # hecho
		return "El prefijo y/o sufijo no puede estar junto a ese elemento"
	elif code == 7: # hecho
		return "El elemento no puede ser abreviado"
	elif code == 8:
		return "El elemento tiene un solo átomo de hidrógeno"
	elif code == 22:
		return "No se ha recibido ningún dato"
	else:
		return None


def getvalencia(elemento):
	with open('tabla.json', 'r') as f:
		data = json.load(f)
	return data["valencias"][elemento]["valencia"]

inorganica = Blueprint("inorganica", __name__)

@inorganica.route("/crash")
def crash():
	with open("crashfunc.json") as f: # Función hecha para crashear
		data = json.load(f)
	return data

@inorganica.route("/error")
def error():
	return render_template("error.html", code=000, descripción="Ninguna")

@inorganica.route("/", methods=["GET"])
def index():
    try:
        nombre = request.form["nombre"]
        return render_template("index.html", nombre=nombre)
    except:
        return render_template("index.html")

@inorganica.route("/inicio")
def inicio():
    return redirect("/")

@inorganica.route("/tutorial")
def tutorial():
	return render_template("write/tutorial.html")

@inorganica.route("/ayuda")
def ayuda():
	return render_template("write/ayuda.html")


@inorganica.route("/about", methods=["GET"])
def about():
	return render_template("about.html")

@inorganica.route("/formularoxido", methods=["GET"])
def oxido():
	session.clear()
	return render_template("oxido.html")

@inorganica.route("/oxidoformulado", methods=["POST", "GET"])
def formularoxido():
	print (session)
	try:
		beta = session["on"]
		print("on")
		datos = session["data"]
	except:
		print ("Beta false")
		beta = False
	if not beta == True:
		try:
			elemento = request.form['metal']
			valencia = request.form['valencia']
		except:
			return render_template('405.html')
	elif beta == True:
		elemento = datos["elemento"]
		valencia = datos["valencia"]
	try:
		valencia = int(valencia)
	except:
		pass
	if elemento == "":
		return render_template("error.html", code=1, descripción=errordesc(1))

	with open('tabla.json', 'r') as f:
		data = json.load(f)
	if not elemento in data["valencias"] and not elemento in data["valencias2"]:
		return render_template("error.html", code=2, descripción=errordesc(2))
		# Elemento no encontrado
	if elemento in data["valencias"]:
		val1 = data["valencias"][elemento]["valencia"]
		elemento1 = data["valencias"][elemento]["símbolo"]
		nombre1 = data["valencias"][elemento]["nombre"]
		fija = True
	else:
		if not valencia in data["valencias2"][elemento]["valencia"]:
			return render_template("error.html", code=3, descripción=errordesc(3))
			# La valencia no corresponde
		val1 = valencia
		elemento1 = data["valencias2"][elemento]["símbolo"]
		nombre1 = data["valencias2"][elemento]["nombre"]
		fija = False

	
	val2 = 2	
	elemento2 = "O"

	# Simplificación
	if val1 == val2:
		val1 = 1
		val2 = 1
	elif val1%3 == 0 and val2%3 == 0:
		val1 = val1/3
		val2 = val2/3
	elif val1%2 == 0 and val2%2 == 0:
		val1 = val1/2
		val2 = val2/2
	
	val1 = int(val1)
	val2 = int(val2)
		
	# se formula
	final1 = val2
	final2 = val1

	if final1 == 1:
		final1 = ""
	if final2 == 1:
		final2 = ""

	
	if not fija == True:
		Forma = " ("+NRomano(valencia)+")"
	else:
		Forma = ""
	nameformula = f"Óxido de {nombre1}{Forma}"
	fórmula = elemento1+str(final1)+elemento2+str(final2)
	session["on"] = False
	session["data"] = ""
	session["nombre"] = ""
	
	#final = (nameformula+": "+elemento1+str(final1)+elemento2+str(final2))
	return render_template("oxido.html", method="POST", fórmula=fórmula, nombre=nameformula)

@inorganica.route("/formularhidruro", methods=["GET"])
def hidruro():
	session.clear()
	return render_template("hidruro.html")

@inorganica.route("/hidruroformulado", methods=["POST", "GET"])
def formularhidruro():
	try:
		beta = session["on"]
		datos = session["data"]
	except:
		beta = False
	if not beta == True:
		try:
			elemento = request.form['metal']
			valencia = request.form['valencia']
		except:
			return render_template('405.html')
	elif beta == True:
		elemento = datos["elemento"]
		valencia = datos["valencia"]
	try:
		valencia = int(valencia)
	except:
		pass
	if elemento == "":
		return render_template("error.html", code=1, descripción=errordesc(1))
	with open('tabla.json', 'r') as f:
		data = json.load(f)
	if not elemento in data["valencias"] and not elemento in data["valencias2"]:
		return render_template("error.html", code=2, descripción=errordesc(2))
		# Elemento no encontrado
	if elemento in data["valencias"]:
		val1 = data["valencias"][elemento]["valencia"]
		sim1 = data["valencias"][elemento]["símbolo"]
		nombre1 = data["valencias"][elemento]["nombre"]
		fija = True
	else:
		if not valencia in data["valencias2"][elemento]["valencia"]:
			return render_template("error.html", code=3, descripción=errordesc(3))
			# La valencia no corresponde
		val1 = valencia
		sim1 = data["valencias2"][elemento]["símbolo"]
		nombre1 = data["valencias2"][elemento]["nombre"]
		fija = False

	sim2 = "H"
	val2 = 1
	#print (f"Valencia de {elemento}: {val1}")

	# Formular
	final1 = val2
	final2 = val1

	if final1 == 1:
		final1 = ""
	if final2 == 1:
		final2 = ""

	
	if not fija == True:
		Forma = " ("+NRomano(val1)+")"
	else:
		Forma = ""
	nameformula = f"Hidruro de {nombre1}{Forma}"
	fórmula = sim1+str(final1)+sim2+str(final2)
	session["on"] = False
	session["data"] = ""
	session["nombre"] = ""
	#final = (nameformula+": "+sim1+str(final1)+sim2+str(final2))
	return render_template("hidruro.html", method="POST", fórmula=fórmula, nombre=nameformula, valencia=valencia)

@inorganica.route("/formularhidroxido", methods=["GET"])
def hidroxido():
	session.clear()
	return render_template("hidroxido.html")

@inorganica.route("/hidroxidoformulado", methods=["POST", "GET"])
def formularhidroxido():
	try:
		beta = session["on"]
		datos = session["data"]
	except:
		beta = False
	if not beta == True:
		try:
			elemento = request.form['metal']
			valencia = request.form['valencia']
		except:
			return render_template('405.html')
	elif beta == True:
		elemento = datos["elemento"]
		valencia = datos["valencia"]
	try:
		valencia = int(valencia)
	except:
		pass
	if elemento == "":
		return render_template("error.html", code=1, descripción=errordesc(1))
	with open('tabla.json', 'r') as f:
		data = json.load(f)
	if not elemento in data["valencias"] and not elemento in data["valencias2"]:
		print ("1")
		return render_template("error.html", code=2, descripción=errordesc(2))
		
		#elemento no encontrado
	if elemento in data["valencias"]:
		val1 = data["valencias"][elemento]["valencia"]
		sim1 = data["valencias"][elemento]["símbolo"]
		nombre1 = data["valencias"][elemento]["nombre"]
		fija = True
	else:
		if not valencia in data["valencias2"][elemento]["valencia"]:
			return render_template("error.html", code=3, descripción=errordesc(3))
			#la valencia no corresponde
		val1 = valencia
		sim1 = data["valencias2"][elemento]["símbolo"]
		nombre1 = data["valencias2"][elemento]["nombre"]
		fija = False

	sim2 = "OH"
	val2 = 1
	#print (f"Valencia de {elemento}: {val1}")

	# Formular
	final1 = val2
	final2 = val1

	if final1 == 1:
		final1 = ""
	if final2 == 1:
		final2 = ""

	
	if not fija == True:
		Forma = " ("+NRomano(val1)+")"
	else:
		Forma = ""

	
	nameformula = f"Hidróxido de {nombre1}{Forma}"
	session["on"] = False
	session["data"] = ""
	session["nombre"] = ""
	if final2 == 1 or final2 == "":
		fórmula = sim1+str(final1)+sim2
		return render_template("hidroxido.html", method="POST", fórmula=fórmula, nombre=nameformula)
	else:
		fórmula = sim1+str(final1)+"("+sim2+")"+str(final2)
		return render_template("hidroxido.html", method="POST", nombre=nameformula, fórmula=fórmula)

@inorganica.route("/formularsalbinaria", methods=["GET"])
def salbinaria():
	session.clear()
	return render_template("salbinaria.html")

@inorganica.route("/salbinariaformulada", methods=["POST", "GET"])
def formularsalbinaria():
	try:
		beta = session["on"]
		datos = session["data"]
	except:
		beta = False
	if not beta == True:
		try:
			elemento1 = request.form['elemento1']
			elemento2 = request.form['elemento2']
			valencia = request.form['valencia']
		except:
			return render_template('405.html')
	elif beta == True:
		elemento1 = datos["elemento1"]
		elemento2 = datos["elemento2"]
		valencia = datos["valencia"]
		porcentaje = datos["porcentaje"]
	
	try:
		valencia = int(valencia)
	except:
		pass
	if elemento1 == "" or elemento2 == "":
		return render_template("error.html", code=1, descripción=errordesc(1))
	# La valencia DEBE ser del elemento 2
	valenciaf = valencia
	with open('tabla.json', 'r') as f:
		data = json.load(f)
	if not elemento2 in data["valencias"] and not elemento2 in data["valencias2"]:
		return render_template("error.html", code=2, descripción=errordesc(2))
		
	if elemento2 in data["valencias"]:
		val2 = data["valencias"][elemento2]["valencia"]
		elemento2 = data["valencias"][elemento2]["símbolo"]
		nombre2 = data["valencias"][elemento2]["nombre"]
		fija = True
	else:
		if not (valencia) in data["valencias2"][elemento2]["valencia"]:
			return render_template("error.html", code=2, descripción=errordesc(2))
		val2 = valencia
		nombre2 = data["valencias2"][elemento2]["nombre"]
		fija = False


		
	if not elemento1 in data["valencias"]:
		return render_template("error.html", code=4, descripción=errordesc(4)) #Debe tener valencia FIJA
	val1 = data["valencias"][elemento1]["valencia"]
	elemento1 = data["valencias"][elemento1]["símbolo"]
	nombre1 = data["valencias"][elemento1]["nombre"]

	# val1 y val2, simplicación
	if val1 == val2:
		val1 = 1
		val2 = 1
	elif val1%4 == 0 and val2%4 == 0:
		val1 = val1/4
		val2 = val2/4
	elif val1%3 == 0 and val2%3 == 0:
		val1 = val1/3
		val2 = val2/3
	elif val1%2 == 0 and val2%2 == 0:
		val1 = val1/2
		val2 = val2/2

	val1 = int(val1)
	val2 = int(val2)
		
	# Formulación
	final1 = val2
	final2 = val1

	if final1 == 1 or final1 == int(1):
		final1 = ""
	if final2 == 1 or final2 == int(1):
		final2 = ""


	if not fija == True:
		Forma = " ("+NRomano(valenciaf)+")"
	else:
		Forma = ""

	
	if not nombre1 in data["abreviado"]:
		return render_template("error.html", code=7, descripción=errordesc(7))

	abreviado = data["abreviado"][nombre1]+"uro"
	if abreviado == "sulfururo":
		abreviado = "sulfuro"

	nameformula = f"{abreviado.capitalize()} de {nombre2}{Forma}"
	if beta == True:
		nameformula = nameformula+f" ({porcentaje} de confirmación)"
	
	fórmula = elemento2+str(final2)+elemento1+str(final1)
	session["on"] = False
	session["data"] = ""
	session["nombre"] = ""
	return render_template("salbinaria.html", method="POST", fórmula=fórmula, nombre=nameformula)

@inorganica.route("/formularacido", methods=["GET"])
def acido():
	session.clear()
	return render_template("acido.html")

@inorganica.route("/acidoformulado", methods=["POST", "GET"])
def acidoformulado():
	procedimientos = {}
	try:
		beta = session["on"]
		datos = session["data"]
	except:
		beta = False
	if not beta == True:
		try:
			elemento1 = request.form['elemento']
			prefijo = request.form['prefijo']
			sufijo = request.form['sufijo']
			prefijoespecial = request.form['prefijoespecial']
		except:
			return render_template('405.html')
	elif beta == True:
		elemento1 = datos["elemento"]
		prefijo = datos["prefijo"]
		sufijo = datos["sufijo"]
		prefijoespecial = datos["prefEspecial"]
		porcentaje = datos["porcentaje"]
	try:
		prefijo = int(prefijo)
	except:
		pass
	try:
		sufijo = int(sufijo)
	except:
		pass
	try:
		prefijoespecial = int(prefijoespecial)
	except:
		pass
		
	if elemento1 == "":
		return render_template("error.html", code=1, descripción=errordesc(1))
	elif prefijo == "" and sufijo == "":
		return render_template("error.html", code=1, descripción=errordesc(1))

	if prefijoespecial == "" or prefijoespecial == "Orto":
		prefijoespecial = 3
	elif prefijoespecial == "Meta":
		prefijoespecial = 1
	elif prefijoespecial == "Piro":
		prefijoespecial = 2

	try:
		prefijoespecial = int(prefijoespecial)
	except:
		prefijoespecial = 3

	with open('tabla.json', 'r') as f:
		data = json.load(f)
	if not elemento1 in data["lista"]:
		return render_template("error.html", code=5, descripción=errordesc(5))
	nombre1 = data["valencias"][elemento1]["nombre"]
	abrv = data["abreviado"][nombre1]
	pref = prefijo
	suf = sufijo
	full = pref+"-"+suf

	try:
		val1 = data["ácidos"][full][elemento1]
	except:
		return render_template("error.html", code=6, descripción=errordesc(6))

	# Primer paso: generar el óxido

	val2 = 2	
	elemento2 = "O"

	# Simplificación
	procedimientos["simp1"] = elemento1+str(val2)+elemento2+str(val1)+" = "
	if val1 == val2:
		val1 = 1
		val2 = 1
	elif val1%3 == 0 and val2%3 == 0:
		val1 = val1/3
		val2 = val2/3
	elif val1%2 == 0 and val2%2 == 0:
		val1 = val1/2
		val2 = val2/2
	
	val1 = int(val1)
	val2 = int(val2)
		
	# Se formula
	semi1 = val2
	semi2 = val1
	procedimientos["simp1"] = procedimientos["simp1"]+elemento1+str(semi1)+elemento2+str(semi2)

	átomosH = 2
	átomosO = 1

	# Segundo paso: Obtener el ácido
	prefEspecial = ""
	temp = "+ H2O"
	if elemento1 in data["especiales"]:
		if prefijoespecial == 1: # Meta
			átomosH = átomosH
			átomosO = átomosO
			prefEspecial = "Meta"
			temp = "+ H2O"
		elif prefijoespecial == 2: # Piro
			átomosH = átomosH*2
			átomosO = átomosO*2
			#print (átomosO)
			prefEspecial = "Piro"
			temp = "+ 2(H2O)"
		elif prefijoespecial == 3: # (Orto)
			átomosH = átomosH*3
			átomosO = átomosO*3
			prefEspecial = "(Orto)"
			temp = "+ 3(H2O)"
	finalO = semi2 + átomosO
	finalH = átomosH
	final1 = semi1
	procedimientos["formular"] = elemento1+str(semi1)+"O"+str(semi2)+" "+temp
	procedimientos["ácido"] = "H"+str(finalH)+elemento1+str(final1)+"O"+str(finalO)
	
	# Simplificar
	if finalO == finalH == final1:
		finalO = 1
		finalH = 1
		final1 = 1
	elif finalO%3 == 0 and finalH%3 == 0 and final1%3 == 0:
		finalO = finalO/3
		finalH = finalH/3
		final1 = final1/3
	elif finalO%2 == 0 and finalH%2 == 0 and final1%2 == 0:
		finalO = finalO/2
		finalH = finalH/2
		final1 = final1/2
	#print (finalO)


	finalH = int(finalH)
	final1 = int(final1)
	finalO = int(finalO)
	procedimientos["ácido"] = procedimientos["ácido"] + " = " + "H"+str(finalH)+elemento1+str(final1)+"O"+str(finalO)

	if final1 == 1:
		final1 = ""
	if finalH == 1:
		finalH = ""
	if finalO == 1:
		finalO = ""

	if abrv == "fosf":
		abrv = "fosfor"
	elif suf == "ico":
		if abrv == "arseni":
			abrv = "arsen"
		elif abrv == "seleni":
			abrv = "selen"
		elif abrv == "antimoni":
			abrv == "antimon"

	if pref == "hipo":
			if abrv == "oxigen":
				abrv = "xigen"
	if pref == "" and prefEspecial == "Meta":
			if abrv == "antimoni":
				abrv = "ntimoni"
			elif abrv == "arseni":
				abrv = "rseni"

	if not prefEspecial == "":
		prefEspecial = prefEspecial.capitalize()
	elif not pref == "":
		pref = pref.capitalize()
	else:
		abrv = abrv.capitalize()

	nombreÁcido = f"Ácido {prefEspecial}{pref}{abrv}{suf}"
	fórmula = f"H{finalH}{elemento1}{final1}{elemento2}{finalO}"
	if beta == True:
		nombreÁcido = nombreÁcido+f" {porcentaje} de confirmación"
	session["on"] = False
	session["data"] = ""
	session["nombre"] = ""
	#final = (nombreÁcido+": "+fórmula)
	return render_template("acido.html", method="POST", fórmula=fórmula, nombre=nombreÁcido, simp1=procedimientos["simp1"], formular=procedimientos["ácido"], óxido=procedimientos["formular"])

@inorganica.route("/reset")
def reset():
	session["on"] = False
	session["Beta"] = False
	return ("Reseteado")

@inorganica.route("/formularsaloxial", methods=["GET"])
def saloxial():
	return render_template("saloxial.html")

@inorganica.route("/saloxialformulada", methods=["POST", "GET"])
def saloxialformulada():
	procedimientos = {}
	try:
		beta = session["on"]
		datos = session["data"]
	except:
		beta = False
	if not beta == True:
		try:
			prefijoespecial = request.form['prefijoespecial']
			prefijo = request.form['prefijo']
			sufijo = request.form['sufijo']
			elemento1 = request.form['elemento']
			elemento4 = request.form['metal']
			valencia4 = request.form['valencia']

		except:
			return render_template('405.html')
	elif beta == True:
		elemento1 = datos["elemento1"]
		prefijo = datos["prefijo"]
		sufijo = datos["sufijo"]
		prefijoespecial = datos["prefEspecial"]
		elemento4 = datos["elemento2"]
		valencia4 = datos["valencia"]
		porcentaje = datos["porcentaje"]
		#print (str(prefijoespecial))
		if prefijoespecial == "" or prefijoespecial == None:
			prefijoespecial = 3
	
	try:
		prefijo = int(prefijo)
	except:
		pass
	try:
		sufijo = int(sufijo)
	except:
		pass
	try:
		prefijoespecial = int(prefijoespecial)
	except:
		pass
	try:
		valencia4 = int(valencia4)
	except:
		pass
	
	if elemento1 == "" or elemento4 == "":
		return render_template("error.html", code=1, descripción=errordesc(1))
	elif prefijo == "" and sufijo == "":
		return render_template("error.html", code=1, descripción=errordesc(1))

	with open('tabla.json', 'r') as f:
		data = json.load(f)
	if not elemento1 in data["lista"]:
		return render_template("error.html", code=5, descripción=errordesc(5))
	nombre1 = data["valencias"][elemento1]["nombre"]
	abrv = data["abreviado"][nombre1]
	pref = prefijo
	suf = sufijo
	full = pref+"-"+suf
	if not elemento4 in data["valencias"] and not elemento4 in data["valencias2"]:
		return render_template("error.html", code=2, descripción=errordesc(2))
		# elemento4 no encontrado
	if elemento4 in data["valencias"]:
		val4 = data["valencias"][elemento4]["valencia"]
		elemento4 = data["valencias"][elemento4]["símbolo"]
		nombre4 = data["valencias"][elemento4]["nombre"]
		fija = True
	else:
		if not valencia4 in data["valencias2"][elemento4]["valencia"]:
			return render_template("error.html", code=3, descripción=errordesc(3))
			# La valencia no corresponde
		val4 = valencia4
		elemento4 = data["valencias2"][elemento4]["símbolo"]
		nombre4 = data["valencias2"][elemento4]["nombre"]
		fija = False

	try:
		val1 = data["sales"][full][elemento1]
	except:
		return render_template("error.html", code=6, descripción=errordesc(6))
	# Primer paso: generar el óxido

	val2 = 2	
	elemento2 = "O"
	procedimientos["all"] = elemento1+str(val2)+elemento2+str(val1)

	# Simplificación
	if val1 == val2:
		val1 = 1
		val2 = 1
	elif val1%3 == 0 and val2%3 == 0:
		val1 = val1/3
		val2 = val2/3
	elif val1%2 == 0 and val2%2 == 0:
		val1 = val1/2
		val2 = val2/2
	
	val1 = int(val1)
	val2 = int(val2)
		
	# Se formula
	semi1 = val2
	semi2 = val1
	procedimientos["all"] = procedimientos["all"] + " = " + elemento1+str(semi1)+elemento2+str(semi2)

	átomosH = 2
	átomosO = 1

	# Segundo paso: Obtener el ácido
	prefEspecial = ""
	temp = "+ H2O"
	if elemento1 in data["especiales"]:
		if prefijoespecial == 1: #Meta
			átomosH = átomosH
			átomosO = átomosO
			prefEspecial = "Meta"
		elif prefijoespecial == 2: #Piro
			átomosH = átomosH*2
			átomosO = átomosO*2
			prefEspecial = "Piro"
			temp = "+ 2(H2O)"
		elif prefijoespecial == 3: #(Orto)
			átomosH = átomosH*3
			átomosO = átomosO*3
			prefEspecial = "(Orto)"
			temp = "+ 3(H2O)"
	finalO = semi2 + átomosO
	finalH = átomosH
	final1 = semi1
	procedimientos["all"] = procedimientos["all"]+" "+temp+" -> "+"H"+str(finalH)+elemento1+str(final1)+"O"+str(finalO)
	
	# Simplificar
	if finalO == finalH == final1:
		finalO = 1
		finalH = 1
		final1 = 1
	elif finalO%4 == 0 and finalH%4 == 0 and final1%4 == 0:
		finalO = finalO/4
		finalH = finalH/4
		final1 = final1/4
	elif finalO%3 == 0 and finalH%3 == 0 and final1%3 == 0:
		finalO = finalO/3
		finalH = finalH/3
		final1 = final1/3
	elif finalO%2 == 0 and finalH%2 == 0 and final1%2 == 0:
		finalO = finalO/2
		finalH = finalH/2
		final1 = final1/2


	finalH = int(finalH)
	final1 = int(final1)
	finalO = int(finalO)
	procedimientos["all"] = procedimientos["all"]+" = "+"H"+str(finalH)+elemento1+str(final1)+"O"+str(finalO)
	

	# Cuarto paso, intercambiar el hidrógeno por el elemento4
	# Simplificar H con val4
	#finalH = int(finalH)
	#val4 = int(val4)
	if val4 == 1:
		procedimientos["all"] = procedimientos["all"] + " (sal) "+elemento4+str(finalH)+elemento1+str(final1)+"O"+str(finalO)
	else:
		procedimientos["all"] = procedimientos["all"] + " (sal) "+elemento4+str(finalH)+"("+elemento1+str(final1)+"O"+str(finalO)+")"+str(val4)

	try:
		finalH = int(finalH)
		val4 = int(val4)
	except:
		return render_template("error.html", code=6, descripción=errordesc(6))

	if finalH == val4:
		valencia4 = 1
		finalH = 1
	elif finalH%4 == 0 and val4%4 == 0:
		valencia4 = valencia4/4
		finalH = finalH/4
	elif finalH%3 == 0 and val4%3 == 0:
		valencia4 = valencia4/3
		finalH = finalH/3
	elif finalH%2 == 0 and val4%2 == 0:
		valencia4 = valencia4/2
		finalH = finalH/2
	val4 = valencia4

	finalH = int(finalH)
	if not val4 == "":
		val4 = int(val4)

	if val4 == 1:
		procedimientos["all"] = procedimientos["all"] + " = "+elemento4+str(finalH)+elemento1+str(final1)+"O"+str(finalO)
	else:
		procedimientos["all"] = procedimientos["all"] + " = "+elemento4+str(finalH)+"("+elemento1+str(final1)+"O"+str(finalO)+")"+str(val4)
	

	if final1 == 1:
		final1 = ""
	if finalH == 1:
		finalH = ""
	if finalO == 1:
		finalO = ""
	num4 = val4
	if val4 == 1:
		val4 = ""

	#if abrv == "fosf":
	#	abrv = "fosfor"
	if abrv == "sulfur":
		abrv = "sulf"
	if suf == "ito":
		if abrv == "arseni":
			abrv = "arsen"
		elif abrv == "seleni":
			abrv = "selen"
		elif abrv == "antimoni":
			abrv == "antimon"
	if pref == "hipo":
			if abrv == "oxigen":
				abrv = "xigen"
	if pref == "" and prefEspecial == "Meta":
			if abrv == "antimoni":
				abrv = "ntimoni"
			elif abrv == "arseni":
				abrv = "rseni"

	if not fija == True:
		Forma = " ("+NRomano(num4)+")"
	else:
		Forma = ""

	if not prefEspecial == "":
		prefEspecial = prefEspecial.capitalize()
	elif not pref == "":
		pref = pref.capitalize()
	else:
		abrv = abrv.capitalize()

	nombreSal = f"{prefEspecial}{pref}{abrv}{suf} de {nombre4}{Forma}"
	if beta == True:
		nombreSal = nombreSal + f" ({porcentaje} de confirmación)"
	if val4 == "":
		fórmula = f"{elemento4}{finalH}{elemento1}{final1}{elemento2}{finalO}"
	else:
		fórmula = f"{elemento4}{finalH}({elemento1}{final1}{elemento2}{finalO}){val4}"
	session["on"] = False
	session["data"] = ""
	session["nombre"] = ""
	return render_template("saloxial.html", method="POST", nombre=nombreSal, fórmula=fórmula, all=procedimientos["all"])


@inorganica.route("/formularsalacida", methods=["GET"])
def salacida():
	session.clear()
	return render_template("salacida.html")

@inorganica.route("/salacidaformulada", methods=["POST", "GET"])
def salacidaformulada():
	procedimientos = {}
	try:
		beta = session["on"]
		datos = session["data"]
	except:
		beta = False
	if not beta == True:
		try:
			prefijoespecial = request.form['prefijoespecial']
			prefijo = request.form['prefijo']
			sufijo = request.form['sufijo']
			elemento1 = request.form['elemento']
			elemento4 = request.form['metal']
			valencia4 = request.form['valencia']

		except:
			return render_template('405.html')
	elif beta == True:
		elemento1 = datos["elemento1"]
		prefijo = datos["prefijo"]
		sufijo = datos["sufijo"]
		prefijoespecial = datos["prefEspecial"]
		elemento4 = datos["elemento2"]
		valencia4 = datos["valencia"]
		porcentaje = datos["porcentaje"]
		#print (str(prefijoespecial))
		if prefijoespecial == "" or prefijoespecial == None:
			prefijoespecial = 3
	
	try:
		prefijo = int(prefijo)
	except:
		pass
	try:
		sufijo = int(sufijo)
	except:
		pass
	try:
		prefijoespecial = int(prefijoespecial)
	except:
		pass
	try:
		valencia4 = int(valencia4)
	except:
		pass
	
	if elemento1 == "" or elemento4 == "":
		return render_template("error.html", code=1, descripción=errordesc(1))
	elif prefijo == "" and sufijo == "":
		return render_template("error.html", code=1, descripción=errordesc(1))

	with open('tabla.json', 'r') as f:
		data = json.load(f)
	if not elemento1 in data["lista"]:
		return render_template("error.html", code=5, descripción=errordesc(5))
	nombre1 = data["valencias"][elemento1]["nombre"]
	abrv = data["abreviado"][nombre1]
	pref = prefijo
	suf = sufijo
	full = pref+"-"+suf
	if not elemento4 in data["valencias"] and not elemento4 in data["valencias2"]:
		return render_template("error.html", code=2, descripción=errordesc(2))
		# elemento4 no encontrado
	if elemento4 in data["valencias"]:
		val4 = data["valencias"][elemento4]["valencia"]
		elemento4 = data["valencias"][elemento4]["símbolo"]
		nombre4 = data["valencias"][elemento4]["nombre"]
		fija = True
	else:
		if not valencia4 in data["valencias2"][elemento4]["valencia"]:
			return render_template("error.html", code=3, descripción=errordesc(3))
			# La valencia no corresponde
		val4 = valencia4
		elemento4 = data["valencias2"][elemento4]["símbolo"]
		nombre4 = data["valencias2"][elemento4]["nombre"]
		fija = False

	try:
		val1 = data["sales"][full][elemento1]
	except:
		return render_template("error.html", code=6, descripción=errordesc(6))
	# Primer paso: generar el óxido

	val2 = 2	
	elemento2 = "O"
	procedimientos["all"] = elemento1+str(val2)+elemento2+str(val1)

	# Simplificación
	if val1 == val2:
		val1 = 1
		val2 = 1
	elif val1%3 == 0 and val2%3 == 0:
		val1 = val1/3
		val2 = val2/3
	elif val1%2 == 0 and val2%2 == 0:
		val1 = val1/2
		val2 = val2/2
	
	val1 = int(val1)
	val2 = int(val2)
		
	# Se formula
	semi1 = val2
	semi2 = val1
	procedimientos["all"] = procedimientos["all"] + " = " + elemento1+str(semi1)+elemento2+str(semi2)

	átomosH = 2
	átomosO = 1

	# Segundo paso: Obtener el ácido
	prefEspecial = ""
	temp = "+ H2O"
	if elemento1 in data["especiales"]:
		if prefijoespecial == 1: #Meta
			átomosH = átomosH
			átomosO = átomosO
			prefEspecial = "Meta"
		elif prefijoespecial == 2: #Piro
			átomosH = átomosH*2
			átomosO = átomosO*2
			prefEspecial = "Piro"
			temp = "+ 2(H2O)"
		elif prefijoespecial == 3: #(Orto)
			átomosH = átomosH*3
			átomosO = átomosO*3
			prefEspecial = "(Orto)"
			temp = "+ 3(H2O)"
	finalO = semi2 + átomosO
	finalH = átomosH
	final1 = semi1
	procedimientos["all"] = procedimientos["all"]+" "+temp+" -> "+"H"+str(finalH)+elemento1+str(final1)+"O"+str(finalO)
	
	# Simplificar
	if finalO == finalH == final1:
		finalO = 1
		finalH = 1
		final1 = 1
	elif finalO%4 == 0 and finalH%4 == 0 and final1%4 == 0:
		finalO = finalO/4
		finalH = finalH/4
		final1 = final1/4
	elif finalO%3 == 0 and finalH%3 == 0 and final1%3 == 0:
		finalO = finalO/3
		finalH = finalH/3
		final1 = final1/3
	elif finalO%2 == 0 and finalH%2 == 0 and final1%2 == 0:
		finalO = finalO/2
		finalH = finalH/2
		final1 = final1/2


	finalH = int(finalH)
	final1 = int(final1)
	finalO = int(finalO)
	procedimientos["all"] = procedimientos["all"]+" = "+"H"+str(finalH)+elemento1+str(final1)+"O"+str(finalO)
	

	# Cuarto paso, restarle 1 a los átomos de H
	# De tal forma que elemento4 (ácido) val4
	if finalH == 1:
		return render_template("error.html", code=8, descripción=errordesc(8))
	finalH -= 1
	if val4 == 1:
		procedimientos["all"] = procedimientos["all"] + " (sal) "+elemento4+"H"+str(finalH)+elemento1+str(final1)+"O"+str(finalO)
	else:
		procedimientos["all"] = procedimientos["all"] + " (sal) "+elemento4+"("+"H"+str(finalH)+elemento1+str(final1)+"O"+str(finalO)+")"+str(val4)

	try:
		finalH = int(finalH)
		val4 = int(val4)
	except:
		return render_template("error.html", code=6, descripción=errordesc(6))


	finalH = int(finalH)
	if not val4 == "":
		val4 = int(val4)

	if final1 == 1:
		final1 = ""
	if finalH == 1:
		finalH = ""
	if finalO == 1:
		finalO = ""
	num4 = val4
	if val4 == 1:
		val4 = ""

	#if abrv == "fosf":
	#	abrv = "fosfor"
	if abrv == "sulfur":
		abrv = "sulf"
	if suf == "ito":
		if abrv == "arseni":
			abrv = "arsen"
		elif abrv == "seleni":
			abrv = "selen"
		elif abrv == "antimoni":
			abrv == "antimon"
	if pref == "hipo":
			if abrv == "oxigen":
				abrv = "xigen"
	if pref == "" and prefEspecial == "Meta":
			if abrv == "antimoni":
				abrv = "ntimoni"
			elif abrv == "arseni":
				abrv = "rseni"

	if not fija == True:
		Forma = " ("+NRomano(num4)+")"
	else:
		Forma = ""

	if not prefEspecial == "":
		prefEspecial = prefEspecial.capitalize()
	elif not pref == "":
		pref = pref.capitalize()
	else:
		abrv = abrv.capitalize()

	nombreSal = f"Bi{prefEspecial}{pref}{abrv}{suf} de {nombre4}{Forma}"
	if beta == True:
		nombreSal = nombreSal + f" ({porcentaje} de confirmación)"
	if val4 == "":
		fórmula = f"{elemento4}H{finalH}{elemento1}{final1}{elemento2}{finalO}"
	else:
		fórmula = f"{elemento4}(H{finalH}{elemento1}{final1}{elemento2}{finalO}){val4}"
	session["on"] = False
	session["data"] = ""
	session["nombre"] = ""
	return render_template("salacida.html", method="POST", nombre=nombreSal, fórmula=fórmula, all=procedimientos["all"])