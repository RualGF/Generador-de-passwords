import random
import string

from fastapi import FastAPI, HTTPException, Query, Body

app = FastAPI()

@app.get("/generar")
def generar_contrasena(longitud_min: int = Query(12, ge=4, description="Longitud mínima de la contraseña (mínimo 4)"), longitud_max: int = Query(24, ge=4, description="Longitud máxima de la contraseña")):
    """
    Genera una contraseña segura que cumple con los siguientes criterios:
    - Longitud entre longitud_min y longitud_max.
    - Incluye al menos una minúscula, una mayúscula, un número y un símbolo.
    """
    # Usamos el módulo string para una definición estándar y más limpia
    letras_minusculas = string.ascii_lowercase
    letras_mayusculas = string.ascii_uppercase
    numeros = string.digits # Caracteres numéricos
    simbolos = "!@#$%^&*()-_+={}[]:;'<>,.?/\\|~`" # Caracteres especiales definidos por el usuario
    
    # --- Validación de la lógica de negocio ---
    if longitud_min > longitud_max:
        raise HTTPException(status_code=400, detail="La longitud mínima no puede ser mayor que la máxima.")

    # Conjunto completo de caracteres para el resto de la contraseña
    todos_los_caracteres = letras_minusculas + letras_mayusculas + numeros + simbolos
    
    # 1. Garantizamos que la contraseña contenga al menos un carácter de cada tipo
    lista_caracteres = [
        random.choice(letras_minusculas),
        random.choice(letras_mayusculas),
        random.choice(numeros),
        random.choice(simbolos)
    ]
    
    # 2. Rellenamos el resto de la contraseña hasta alcanzar una longitud aleatoria
    # La longitud final siempre estará entre longitud_min y longitud_max
    longitud_final = random.randint(longitud_min, longitud_max)
    for _ in range(longitud_final - len(lista_caracteres)):
        lista_caracteres.append(random.choice(todos_los_caracteres))
        
    # 3. Mezclamos los caracteres para que los primeros 4 no sean siempre los mismos tipos
    random.shuffle(lista_caracteres)
    # 4. Unimos la lista de caracteres para formar el string final.
    # "".join(lista_caracteres) convierte la lista de caracteres en una única cadena de texto.
    return "".join(lista_caracteres) # Devuelve un string, no una lista.

@app.post("/verificar")
def verificar_contrasena(contrasena: str = Body(..., description="La contraseña a verificar"), longitud_min: int = 12, longitud_max: int = 24):
    """
    Comprueba si una contraseña cumple con los criterios de seguridad definidos.
    Devuelve True si es válida, False en caso contrario.
    """
    # Criterio 1: Longitud
    if not (longitud_min <= len(contrasena) <= longitud_max): # Comprueba que la longitud esté en el rango.
        # El mensaje de error se puede quitar si solo se necesita el valor booleano de retorno.
        # print(f"Error: La longitud ({len(contrasena)}) no está entre {longitud_min} y {longitud_max}.")
        return False
    
    # Criterio 2: Complejidad (al menos un carácter de cada tipo)
    # Se usa el mismo conjunto de símbolos que en la generación para consistencia.
    simbolos_requeridos = "!@#$%^&*()-_+={}[]:;'<>,.?/\\|~`"
    if not any(c in string.ascii_lowercase for c in contrasena): return False
    if not any(c in string.ascii_uppercase for c in contrasena): return False
    if not any(c in string.digits for c in contrasena): return False
    if not any(c in simbolos_requeridos for c in contrasena): return False
    
    # Si pasa todas las comprobaciones, es válida
    return True