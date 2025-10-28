import secrets
import string
import random

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI()

# Modelo Pydantic para la respuesta
class PasswordResponse(BaseModel):
    password: str
    longitud: int

# Modelo Pydantic para la solicitud de verificación
class VerificationRequest(BaseModel):
    password: str

# Modelo Pydantic para la respuesta de verificación
class VerificationResponse(BaseModel):
    es_valido: str
    fallo: list[str] = []

@app.get("/generar", response_model = PasswordResponse)
def generar_contrasena(longitud_min: int = Query(12, ge = 4, description = "Longitud mínima de la contraseña (mínimo 4)"), 
                       longitud_max: int = Query(24, ge = 4, description = "Longitud máxima de la contraseña")):
    """
    Genera una contraseña segura que cumple con los siguientes criterios:
    - Longitud entre longitud_min y longitud_max.
    - Incluye al menos una minúscula, una mayúscula, un número y un símbolo.
    """
    # Usamos el módulo string para una definición estándar y más limpia
    letras_minusculas = string.ascii_lowercase
    letras_mayusculas = string.ascii_uppercase
    numeros = string.digits 
    simbolos = "!@#$%^&*()-_+={}[]:;'<>,.?/\\|~`"
    
    # --- Validación de la lógica de negocio ---
    if longitud_min > longitud_max:
        raise HTTPException(status_code = 400, detail = "La longitud mínima no puede ser mayor que la máxima.")

    # Conjunto completo de caracteres para el resto de la contraseña
    todos_los_caracteres = letras_minusculas + letras_mayusculas + numeros + simbolos
    
    # Garantizamos que la contraseña contenga al menos un carácter de cada tipo
    lista_caracteres = [
        secrets.choice(letras_minusculas),
        secrets.choice(letras_mayusculas),
        secrets.choice(numeros),
        secrets.choice(simbolos)
    ]
    
    # Rellenamos el resto de la contraseña hasta alcanzar una longitud aleatoria, que siempre estará entre longitud_min y longitud_max
    longitud_final = secrets.randbelow(longitud_max - longitud_min + 1) + longitud_min
    for _ in range(longitud_final - len(lista_caracteres)):
        lista_caracteres.append(secrets.choice(todos_los_caracteres))
        
    #  Mezclamos los caracteres para que los primeros 4 no sean siempre los mismos tipos
    random.shuffle(lista_caracteres)
    
    # Unimos la lista de caracteres para formar el string final.
    password_generado = "".join(lista_caracteres)
    
    # Devolvemos una instancia del modelo Pydantic, que FastAPI convertirá a JSON.
    return PasswordResponse(password = password_generado, longitud = len(password_generado))

@app.post("/verificar", response_model = VerificationResponse)
def verificar_contrasena(request: VerificationRequest, longitud_min: int = Query(12, ge = 4, description = "Longitud mínima requerida"), 
                         longitud_max: int = Query(24, ge = 4, description = "Longitud máxima requerida")):
    """
    Comprueba si una contraseña cumple con los criterios de seguridad definidos.
    Devuelve un objeto JSON detallando el resultado de la validación.
    """
    contrasena = request.password
    fallos = []

    # Criterio 1: Longitud
    if not (longitud_min <= len(contrasena) <= longitud_max):
        fallos.append(f"La longitud debe estar entre {longitud_min} y {longitud_max} caracteres.")
    
    # Criterio 2: Complejidad (al menos un carácter de cada tipo)
    simbolos_requeridos = "!@#$%^&*()-_+={}[]:;'<>,.?/\\|~`"
    if not any(c in string.ascii_lowercase for c in contrasena):
        fallos.append("Debe contener al menos una letra minúscula.")
    if not any(c in string.ascii_uppercase for c in contrasena):
        fallos.append("Debe contener al menos una letra mayúscula.")
    if not any(c in string.digits for c in contrasena):
        fallos.append("Debe contener al menos un número.")
    if not any(c in simbolos_requeridos for c in contrasena):
        fallos.append("Debe contener al menos un carácter especial.")
    
    if fallos:
        return VerificationResponse(es_valido = "La contraseña introducida no es válida", fallo = fallos)
    
    return VerificationResponse(es_valido = "La contraseña introducida es válida")