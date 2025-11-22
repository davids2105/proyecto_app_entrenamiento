


def calular_imc(peso, altura):
    imc = round(peso / (altura * altura), 2)
    clasifi = clasificImc(imc)
    return imc, clasifi
    
    
def clasificImc(imc):
    if (imc < 18.5): return "Bajo peso"
    elif (imc < 24.9): return "Peso normal"
    elif (imc < 29.9): return "Sobrepeso"
    else: return "Obesidad";
    
def grasa_corporal(imc, edad, sexo):
    sexo_factor = 1 if sexo.upper() == "M" else 0
    return round(1.20 * imc + 0.23 * edad - 10.8 * sexo_factor - 5.4, 2)

def calcular_tmb(peso, altura_m, edad, sexo):
    altura_cm = altura_m * 100
    
    if sexo.upper() == "M":
        tmb = 88.362 + (13.397 * peso) + (4.799 * altura_cm) - (5.677 * edad)
    else:
        tmb = 447.593 + (9.247 * peso) + (3.098 * altura_cm) - (4.330 * edad)

    return round(tmb, 2)

def calorias_mantenimiento(tmb, nivel_actividad):
    factores = {
        "sedentario": 1.2,
        "ligero": 1.375,
        "moderado": 1.55,
        "intenso": 1.725,
        "muy_intenso": 1.9
    }
    
    factor = factores.get(nivel_actividad.lower(), 1.2)
    return round(tmb * factor, 2)


def calorias_objetivo(tdee, objetivo):
    if objetivo == "bajar_peso":
        return round(tdee - 400, 2)
    elif objetivo == "subir_masa":
        return round(tdee + 300, 2)
    else:  # mantener
        return tdee
    
def peso_saludable(altura_m):
    altura2 = altura_m * altura_m
    peso_min = 18.5 * altura2
    peso_max = 24.9 * altura2
    return round(peso_min, 2), round(peso_max, 2)