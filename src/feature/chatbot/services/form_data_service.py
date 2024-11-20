from feature.chatbot.action.customer.get_customer_action import create_customer_action
from feature.chatbot.models.customer_model import CustomerModel
from feature.chatbot.utils.json_utils import save_to_json

class FormDataService:
    def __init__(self, form_data: dict):
        self.form_data = form_data

    def process_form_data(self):
        """Procesa los datos del formulario."""
        try:
            # Validar datos
            if not self.validate_form_data():
                raise ValueError("Datos inválidos.")

            # Crear cliente
            new_customer = CustomerModel(
                nombre=self.form_data["nombre"],
                identificacion=self.form_data["id"],
                correo=self.form_data["email"],
                correo_verificado=True,
                activo=True
            )
            create_customer_action(new_customer)

            # Guardar los datos en un archivo JSON
            save_to_json(self.form_data)

            print("Formulario procesado correctamente.")
        except Exception as e:
            print(f"Error al procesar los datos del formulario: {e}")

    def validate_form_data(self) -> bool:
        """Valida los datos del formulario."""
        if not self.form_data:
            return False
        if not self.form_data.get("nombre").isalpha():
            return False
        if not self.form_data.get("email"):
            return False
        if not self.form_data.get("id").isdigit():
            return False
        return True
