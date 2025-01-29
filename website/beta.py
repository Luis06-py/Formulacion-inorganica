from flask import Blueprint, render_template, request, redirect, url_for, session
beta = Blueprint("beta", __name__)

import os, json
#os.system("python run.py")
from module2 import NInversa

def getsymbol(name):
    with open ("tabla.json", "r") as f:
        data = json.load(f)
    if name in data["valencias"]:
        return data["valencias"][name]["símbolo"]
    elif name in data["valencias2"]:
        return data["valencias2"][name]["símbolo"]
    else:
        return None
    
def analizar_formula(formula):
    with open ("tabla.json", "r") as f:
        data = json.load(f)
    #print (data["especial"])
    if formula in data["especial"]:
        return {"tipo": "especial", "elemento":data["especial"][formula]}
    abreviaciones = []
    for x in data["abreviado"]:
        abreviaciones.append(data["abreviado"][x])
    pref = ''
    suf = ''
    prefEspecial = ''

    if "uro" in formula and not "Hidruro de" in formula:

        numeros_romanos = ["(I)", "(II)", "(III)", "(IV)", "(V)"]
        for numero_romano in numeros_romanos:
            if numero_romano in formula:
                valencia = NInversa(numero_romano)
                formula = formula.replace(numero_romano, '')
                break
            else:
                valencia = None

        try:
            a = valencia
        except:
            valencia = None
        
        elementos = formula.split("uro")
        elemento1 = elementos[0].strip()
        elemento2 = elementos[1].replace("de ", "")
        elemento2 = elemento2.replace(" ", "").strip()


        mejor_coincidencia = None
        porcentaje_confirmacion = 0.0
        for abreviacion in abreviaciones:
            coincidencias = 0
            for letra in abreviacion:
                if letra in elemento1:
                    coincidencias += 1
                    confirmacion = (coincidencias / len(abreviacion))*100
                    if confirmacion > porcentaje_confirmacion:
                        porcentaje_confirmacion = confirmacion
                        mejor_coincidencia = abreviacion
        
        #elemento1 = data["abreviado"][mejor_coincidencia]
        for x in data["abreviado"]:
            #print (x)
            if mejor_coincidencia == data["abreviado"][x]:
                elemento1 = x
        porcentaje_confirmacion = round(porcentaje_confirmacion, 0)

        return {"tipo":"sal", "elemento1":getsymbol(elemento1), "elemento2":getsymbol(elemento2), "valencia":valencia, "porcentaje":str(porcentaje_confirmacion)+"%"}
        #return elemento1, elemento2, valencia, porcentaje_confirmacion, "% de confirmación"

    if not any(word in formula.lower() for word in ["hidruro", "óxido", "ácido", "hidróxido"]):
        print ("Sal oxisal")

        # Detectar y eliminar números romanos en la variable valencia
        numeros_romanos = ["(I)", "(II)", "(III)", "(IV)", "(V)"]
        for numero_romano in numeros_romanos:
            if numero_romano in formula:
                valencia = NInversa(numero_romano)
                formula = formula.replace(numero_romano, '')
                break

        elemento1 = formula
        try:
            partes = elemento1.split(" de ")
            elemento1 = partes[0]
            elemento2 = partes[1]
            elemento2 = elemento2.replace(" ", "")
        except:
            return None

        if elemento1.lower().startswith("meta"):
            prefEspecial = "Meta"
            elemento1 = elemento1[4:]
        elif elemento1.lower().startswith("piro"):
            prefEspecial = "Piro"
            elemento1 = elemento1[4:]

        if elemento1.lower().startswith("hipo"):
            pref = "Hipo"
            elemento1 = elemento1[4:]
        elif formula.lower().startswith("per"):
            pref = "Per"
            elemento1 = elemento1[3:]

        if elemento1.lower().endswith("ito"):
            suf = "ito"
            elemento1 = elemento1[:-3]
        elif elemento1.lower().endswith("ato"):
            suf = "ato"
            elemento1 = elemento1[:-3]

        elemento1 = elemento1.strip()

        mejor_coincidencia = None
        porcentaje_confirmacion = 0.0
        for abreviacion in abreviaciones:
            coincidencias = 0
            for letra in abreviacion:
                if letra in elemento1:
                    coincidencias += 1
                    confirmacion = (coincidencias / len(abreviacion))*100
                    if confirmacion > porcentaje_confirmacion:
                        porcentaje_confirmacion = confirmacion
                        mejor_coincidencia = abreviacion
        
        #elemento1 = data["abreviado"][mejor_coincidencia]
        for x in data["abreviado"]:
            #print (x)
            if mejor_coincidencia == data["abreviado"][x]:
                elemento1 = x
        try:
            a = valencia
        except:
            valencia = None
        porcentaje_confirmacion = round(porcentaje_confirmacion, 0)
        return {"tipo":"sal oxisal", "elemento1":getsymbol(elemento1), "elemento2":getsymbol(elemento2), "valencia":valencia, "prefijo":pref, "sufijo":suf, "prefEspecial":prefEspecial, "porcentaje":str(porcentaje_confirmacion)+"%"}
        #return elemento1, str(porcentaje_confirmacion), "% de confirmación", pref, suf, prefEspecial, valencia, ">", elemento2

    if formula.startswith("Ácido "):
        elemento = formula
        
        elemento = elemento[6:] #7:

        if elemento.lower().startswith("meta"):
            prefEspecial = "Meta"
            elemento = elemento[4:]
        elif elemento.lower().startswith("piro"):
            prefEspecial = "Piro"
            elemento = elemento[4:]

        if elemento.lower().startswith("hipo"):
            pref = "Hipo"
            elemento = elemento[4:]
        elif elemento.lower().startswith("per"):
            pref = "Per"
            elemento = elemento[3:]

        if elemento.lower().endswith("oso"):
            suf = "oso"
            elemento = elemento[:-3]
        elif elemento.lower().endswith("ico"):
            suf = "ico"
            elemento = elemento[:-3]

        mejor_coincidencia = None
        porcentaje_confirmacion = 0.0
        for abreviacion in abreviaciones:
            coincidencias = 0
            for letra in abreviacion:
                if letra in elemento: 
                    coincidencias += 1
                    confirmacion = (coincidencias / len(abreviacion))*100
                    if confirmacion > porcentaje_confirmacion:
                        porcentaje_confirmacion = confirmacion
                        mejor_coincidencia = abreviacion
        
        #elemento1 = data["abreviado"][mejor_coincidencia]
        for x in data["abreviado"]:
            #print (x)
                if mejor_coincidencia == data["abreviado"][x]:
                    elemento = x
        porcentaje_confirmacion = round(porcentaje_confirmacion, 0)
        return {"tipo":"ácido", "elemento":getsymbol(elemento), "prefijo":pref, "sufijo":suf, "prefEspecial":prefEspecial, "porcentaje":str(porcentaje_confirmacion)+"%"}
        #return elemento, pref, suf, prefEspecial, porcentaje_confirmacion, "% de confirmación"
    
    
    palabras_clave = {
        "Hidruro de": "hidruro",
        "Óxido de": "óxido",
        "Hidróxido de": "hidróxido"
    }
    forma = None
    elemento = None
    valencia = None
    for palabra in palabras_clave:
        if palabra in formula:
            forma = palabras_clave[palabra]
            elemento = formula.split(palabra)[1].strip()
            break

    if forma and elemento:
        numeros_romanos = ["(I)", "(II)", "(III)", "(IV)", "(V)"]
        for numero_romano in numeros_romanos:
            if numero_romano in formula:
                valencia = NInversa(numero_romano)
                elemento = elemento.replace(" "+numero_romano, "")
                break
            else:
                valencia = None

    try:
        a = valencia
    except:
        valencia = None

    if forma == "hidróxido":
        return {"tipo":"hidróxido", "elemento":getsymbol(elemento), "valencia":valencia}
        #return "OH, valencia "+str(valencia)
    elif forma == "óxido":
        return {"tipo":"óxido", "elemento":getsymbol(elemento), "valencia":valencia}
        # O
    elif forma == "hidruro":
        return {"tipo":"hidruro", "elemento":getsymbol(elemento), "valencia":valencia}
        #return "H, valencia "+str(valencia)
    else:
        return {"tipo":None}

def escribe_aqui():
    pass

@beta.route("/formular2", methods=["POST"])
def formular2():
    formula = request.form["fórmula"]
    datos = analizar_formula(formula)
    if datos == None:
        return render_template("error.html", code="22", descripción="Error, ningún dato recibido")
    for x in datos:
        if datos[x] == None:
            datos[x] = ""
    tipo = datos["tipo"]
    session["on"] = True
    session["data"] = datos
    session["nombre"] = formula
    #print(f"Datos {datos}")
    if tipo == "hidróxido":
        elemento = datos["elemento"]
        valencia = datos["valencia"]
        return redirect(url_for("inorganica.formularhidroxido"))
    elif tipo == "óxido":
        elemento = datos["elemento"]
        valencia = datos["valencia"]
        return redirect(url_for("inorganica.formularoxido"))
    elif tipo == "hidruro":
        elemento = datos["elemento"]
        valencia = datos["valencia"]
        return redirect(url_for("inorganica.formularhidruro"))
    elif tipo == "especial":
        elemento = datos["elemento"]
        nombre = formula
        return redirect(url_for('beta.resultado', fórmula=elemento, nombre=nombre))
    elif tipo == "sal":
        elemento1 = datos["elemento1"]
        elemento2 = datos["elemento2"]
        valencia = datos["valencia"]
        porcentaje = datos["porcentaje"]
        return redirect(url_for("inorganica.formularsalbinaria"))
    elif tipo == "sal oxisal":
        elemento1 = datos["elemento1"]
        elemento2 = datos["elemento2"]
        valencia = datos["valencia"]
        prefijo = datos["prefijo"]
        sufijo = datos["sufijo"]
        prefEspecial = datos["prefEspecial"]
        porcentaje = datos["porcentaje"]
        return redirect(url_for("inorganica.saloxialformulada"))
    elif tipo == "ácido":
        elemento = datos["elemento"]
        prefijo = datos["prefijo"]
        sufijo = datos["sufijo"]
        prefEspecial = datos["prefEspecial"]
        porcentaje = datos["porcentaje"]
        return redirect(url_for("inorganica.acidoformulado"))
    else:
        session["on"] = False
        session["data"] = ""
        session["nombre"] = ""
        return render_template("error.html", code="21", descripción="Error, no está bien escrito")
        
   

@beta.route("/resultado", methods=["POST", "GET"])
def resultado():
    fórmula = request.args["fórmula"]
    nombre = request.args["nombre"]
    return render_template("beta/resultado.html", method="POST", fórmula=fórmula, nombre=nombre)