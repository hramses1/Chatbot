from jinja2 import Template

class RenderService:
    @staticmethod
    def render_template(data_cases, user):
        """
        Renderiza la plantilla HTML con los datos de casos dinámicos.
        """
        template_path = "./feature/chatbot/html/plantilla_message.html"

        # Cargar la plantilla HTML
        with open(template_path, "r", encoding="utf-8") as file:
            template_html = file.read()

        # Crear un template Jinja2
        template = Template(template_html)

        # Convertir data_cases a un formato que la plantilla pueda usar
        context = {
            "nombre": user['nombre'],
            "correo": user['correo'],
            "identificacion":user['identificacion'],
            "correo_verificado": user['correo_verificado'],
            "created": user['created'],
            "page": getattr(data_cases, "page", 1),
            "totalPages": getattr(data_cases, "totalPages", 1),
            "totalItems": getattr(data_cases, "totalItems", 0),
            "items": [
                {
                    "fecha_cita": getattr(item, "fecha_cita", ""),
                    "estado_caso": getattr(item, "estado_caso", ""),
                    "observacion": getattr(item, "observacion", ""),
                }
                for item in getattr(data_cases, "items", [])
            ],
        }
        
        # Renderizar la plantilla con los datos
        return template.render(context)
