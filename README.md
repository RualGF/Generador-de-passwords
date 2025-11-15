# Generador y Verificador de Contraseñas Seguras (API FastAPI)

Este proyecto implementa una API RESTful utilizando FastAPI para generar y verificar contraseñas aleatorias que cumplen con criterios de seguridad específicos. Es una herramienta útil para entender cómo se pueden aplicar las mejores prácticas de seguridad y validación en el desarrollo de APIs con Python.
# Generador de Passwords

[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=flat-square&logo=python&logoColor=yellow)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-Server-black?style=flat-square&logo=uvicorn&logoColor=white)](https://www.uvicorn.org/)
[![Pydantic](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json&style=flat-square)](https://pydantic.dev)
[![Secrets](https://img.shields.io/badge/secrets-secure%20random-orange?style=flat-square&logo=python&logoColor=white)](https://docs.python.org/3/library/secrets.html)
[![Random](https://img.shields.io/badge/random-fallback-blue?style=flat-square&logo=python&logoColor=white)](https://docs.python.org/3/library/random.html)
[![String](https://img.shields.io/badge/string-utils-green?style=flat-square&logo=python&logoColor=white)](https://docs.python.org/3/library/string.html)

## 🚀 Características

La API ofrece las siguientes funcionalidades:

-   **Generación de Contraseñas**:
    -   Longitud configurable (mínimo 12, máximo 24 caracteres por defecto).
    -   Garantiza la inclusión de al menos una letra minúscula, una mayúscula, un número y un carácter especial.
    -   Utiliza el módulo `secrets` de Python para una generación criptográficamente segura, lo que la hace adecuada para entornos donde la aleatoriedad impredecible es crucial.
    -   Devuelve la contraseña generada y su longitud en un formato JSON estructurado.
-   **Verificación de Contraseñas**:
    -   Comprueba si una contraseña dada cumple con los mismos criterios de longitud y complejidad.
    -   Devuelve una respuesta detallada en JSON, indicando si la contraseña es válida (`es_valido`) y una lista de los criterios que no cumple (`fallo`) en caso de ser inválida.
-   **Validación Robusta**:
    -   FastAPI y Pydantic se encargan de la validación automática de los parámetros de entrada y los cuerpos de las solicitudes/respuestas, asegurando que los datos sean del tipo y formato esperados.
-   **Documentación Interactiva**:
    -   FastAPI genera automáticamente una documentación interactiva de la API (Swagger UI) accesible en `/docs`, lo que facilita la exploración y prueba de los endpoints.

## 🛠️ Tecnologías Utilizadas

-   **Python 3.13.7**
-   **FastAPI**: Framework web de alto rendimiento para construir APIs.
-   **Pydantic**: Biblioteca para la validación de datos y la gestión de la configuración utilizando type hints de Python.
-   **`secrets`**: Módulo de Python para generar números aleatorios criptográficamente seguros.
-   **`random`**: Módulo de Python para operaciones aleatorias (utilizado para barajar la contraseña generada).

## ⚙️ Instalación y Ejecución

Sigue estos pasos para poner en marcha el proyecto en tu máquina local:

1.  **Clona el repositorio** (o descarga el archivo `main.py`):
    ```bash
    git clone <URL_DE_TU_REPOSITORIO>
    cd generador-contrasenas
    ```

2.  **Crea un entorno virtual** (recomendado):
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # En Linux/macOS
    .venv\Scripts\activate     # En Windows
    ```

3.  **Instala las dependencias**:
    ```bash
    pip install fastapi uvicorn pydantic
    ```

4.  **Ejecuta la aplicación**:
    ```bash
    uvicorn main:app --reload
    ```
    La API estará disponible en `http://127.0.0.1:8000` o en `http://localhost:8000`.

5.  **Accede a la documentación interactiva**:
    Abre tu navegador y visita `http://127.0.0.1:8000/docs` para explorar los endpoints y probar la API.

## 🚀 Endpoints de la API

### 1. Generar Contraseña

-   **URL**: `/generar`
-   **Método**: `GET`
-   **Descripción**: Genera una contraseña aleatoria que cumple con los criterios de seguridad.
-   **Parámetros de Consulta (Query Parameters)**:
    -   `longitud_min` (int, opcional, por defecto 12): Longitud mínima de la contraseña (mínimo 4).
    -   `longitud_max` (int, opcional, por defecto 24): Longitud máxima de la contraseña.
-   **Ejemplo de Respuesta (200 OK)**:
    ```json
    {
      "password": "a5B!c8D?e2F#",
      "longitud": 12
    }
    ```

### 2. Verificar Contraseña

-   **URL**: `/verificar`
-   **Método**: `POST`
-   **Descripción**: Comprueba si una contraseña proporcionada cumple con los criterios de seguridad.
-   **Cuerpo de la Solicitud (Request Body)**:
    ```json
    {
      "password": "tu_contraseña_a_verificar"
    }
    ```
-   **Parámetros de Consulta (Query Parameters)**:
    -   `longitud_min` (int, opcional, por defecto 12): Longitud mínima requerida para la verificación.
    -   `longitud_max` (int, opcional, por defecto 24): Longitud máxima requerida para la verificación.
-   **Ejemplo de Respuesta (200 OK - Válida)**:
    ```json
    {
      "es_valido": true,
      "fallo": []
    }
    ```
-   **Ejemplo de Respuesta (200 OK - Inválida)**:
    ```json
    {
      "es_valido": false,
      "fallo": [
        "La longitud debe estar entre 12 y 24 caracteres.",
        "Debe contener al menos un carácter especial."
      ]
    }
    ```

## 💡 Notas de Implementación

-   **`secrets` vs `random`**: Aunque la especificación inicial mencionaba `random`, se optó por `secrets` para la generación de caracteres debido a su superioridad criptográfica, lo que garantiza una mayor seguridad en las contraseñas generadas. `random.shuffle` se utiliza para mezclar los caracteres, lo cual es seguro en este contexto.
-   **Pydantic Models**: Se utilizan modelos Pydantic (`PasswordResponse`, `VerificationRequest`, `VerificationResponse`) para definir la estructura de los datos de entrada y salida de la API. Esto proporciona validación automática, serialización/deserialización y una excelente documentación en `/docs`.
-   **Validación de Parámetros**: Los parámetros de consulta (`Query`) incluyen validaciones como `ge=4` (mayor o igual a 4), lo que asegura que las longitudes mínimas y máximas sean lógicas y evita errores internos.
-   **Respuestas Detalladas**: El endpoint `/verificar` no solo indica si una contraseña es válida, sino que también proporciona una lista de los criterios que no se cumplen, facilitando la depuración y la retroalimentación al usuario.

## ⚠️ Advertencia de Seguridad

Aunque este proyecto utiliza el módulo `secrets` para la generación de contraseñas, la seguridad de cualquier sistema depende de muchos factores. **No uses este algoritmo directamente para generar contraseñas de uso personal crítico sin una revisión exhaustiva por parte de expertos en seguridad.** Este proyecto está diseñado con fines educativos y de demostración de una API.

