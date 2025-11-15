import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_generar_password():
    response = client.get("/generar?longitud_min=12&longitud_max=16")
    assert response.status_code == 200
    data = response.json()
    assert "password" in data
    assert "longitud" in data
    password = data["password"]
    assert 12 <= data["longitud"] <= 16
    assert any(c.islower() for c in password)
    assert any(c.isupper() for c in password)
    assert any(c.isdigit() for c in password)
    assert any(c in "!@#$%^&*()-_+={}[]:;'<>,.?/\\|~`" for c in password)

def test_verificar_valida():
    response = client.post(
        "/verificar?longitud_min=12&longitud_max=24",
        json={"password": "Valida123!segura"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["es_valido"] == "La contraseña introducida es válida"

def test_verificar_corta():
    response = client.post(
        "/verificar?longitud_min=12&longitud_max=24",
        json={"password": "corta1!"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["es_valido"] == "La contraseña introducida no es válida"
    assert any("longitud" in f.lower() for f in data["fallo"])