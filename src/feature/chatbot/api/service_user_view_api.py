from common.axios import Axios

def get_service_user_for_user_api(user: str):
    ## This function searches for the services of the lawyer sent as a parameter.
    ## user == abogado
    ## Esta funcion busca los servicios del abogado enviados como parametro.
    return Axios().get(f'/collections/usuario_servicio_vista/records?filter=nombre_usuario={user}')

def get_service_user_for_id_specialty_api(id_specialty: str):
    return Axios().get(f"/collections/usuario_servicio_vista/records?filter=(id_especialidad='{id_specialty}')")


def get_customer_state_cases_api(email: str):
    return Axios().get(f"/collections/cliente_caso_correo_vista/records?filter=(correo_cliente='{email}')")