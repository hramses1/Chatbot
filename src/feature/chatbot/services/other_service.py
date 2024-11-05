from feature.chatbot.action.specialty.get_specialties_action import get_specialties_action

def get_welcome_message():
    message = "👋 ¡Bienvenido/a a **Estudio Jurídico Camacho Gomez**! \n"
    message += "\n Nos complace que estés aquí. Somos un equipo dedicado a ofrecerte asesoría y soluciones legales a la medida de tus necesidades."
    message += "\n Nuestro compromiso es acompañarte y brindarte el apoyo que necesitas en cada paso del proceso legal."
    
    #message += "\n\n 👨‍⚖️ Estamos aquí para ayudarte en áreas como:\n\n"
    
    return message

def get_list_options_message():
    message = (
        "Cuéntanos en qué podemos ayudarte, estamos aquí para brindarte apoyo en varias áreas.\n\n"
        "Primero, déjanos presentarte nuestras especialidades para que elijas la que mejor se ajuste a tus necesidades:\n"
    )
    return message

def get_interest_query_message():
    message = (
        "¿En cuál de estas áreas te gustaría consultar y agendar una cita? "
        "Selecciona la que más se ajuste a lo que necesitas, y te ayudaremos a coordinar tu cita lo antes posible. 😊"
    )
    return message

def get_service_details_message(service):
    message = (
        f"⭐ *{service['name']}*\n\n"
        f"📄 *Descripción*: {service['description']}\n"
        f"💰 *Precio*: ${service['price']}\n"
        f"📅 *Disponibilidad*: {'Disponible' if service['status'] else 'No disponible'}\n\n"
        f"Si te interesa este servicio, ¡avísanos y te ayudaremos a agendar tu cita! 😊\n\n"
    )
    return message

def get_specialties_message():
    message = ""
    specialties = get_specialties_action()

    for index, specialty in enumerate(specialties, start=1):
        message += f"{index}. **{specialty.name}** : {specialty.description}\n"
    
    return message

