def NInversa(numero):
	if numero == "I" or numero == "(I)":
		return 1
	elif numero == "II" or numero == '(II)':
		return 2
	elif numero == "III" or numero == "(III)":
		return 3
	elif numero == "IV" or numero == "(IV)":
		return 4
	elif numero == "V" or numero == "(V)":
		return 5
	else:
		return None

def NRomano(numero):
	if numero == 1:
		return "I"
	elif numero == 2:
		return "II"
	elif numero == 3:
		return "III"
	elif numero == 4:
		return "IV"
	elif numero == 5:
		return "V"
	elif numero == 6:
		return "VI"
	elif numero == 7:
		return "VII"
	else:
		return None

