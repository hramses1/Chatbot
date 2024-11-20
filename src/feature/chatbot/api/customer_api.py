from common.axios import Axios
import re

def get_customer_api(email: str):
    return Axios().get(f"/collections/cliente/records?filter=correo='{email}'")

def get_customers_api():
    return Axios().get('/collections/cliente/records?perPage=-1&sort=-created')

def create_customer_api(json=None):
    if not json:
        print("⚠️ No se proporcionaron datos para crear el cliente.")
        return None

    axios = Axios()
    response = axios.post('/collections/cliente/records', json=json)

    if response:
        print("✅ Cliente creado exitosamente.")
        return response
    else:
        print("❌ Error al crear el cliente.")
        return None