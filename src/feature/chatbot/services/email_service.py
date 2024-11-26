import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
from smtplib import SMTP, SMTP_SSL, SMTPException
from dotenv import load_dotenv

# Cargar variables desde el archivo .env
load_dotenv()

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv("SERVER_SMTP")
        self.smtp_port = 465
        self.username = os.getenv("USERNAME_SMTP")
        self.password = os.getenv("PASSWORD_SMTP")

        if not all([self.smtp_server, self.smtp_port, self.username, self.password]):
            raise ValueError("Faltan configuraciones necesarias en el archivo .env")

    def send_email(self, to_email: str, subject: str, html_template: str, attachments: list = None):
        try:
            # Validar y codificar entradas como UTF-8
            to_email = str(to_email).encode("utf-8").decode("utf-8")
            subject = str(subject).encode("utf-8").decode("utf-8")
            html_template = str(html_template).encode("utf-8").decode("utf-8")

            # Crear el mensaje
            message = MIMEMultipart()
            message["Subject"] = Header(subject, "utf-8")
            message["From"] = Header(self.username, "utf-8")
            message["To"] = Header(to_email, "utf-8")
            
            

            # Adjuntar el cuerpo del correo (HTML)
            message.attach(MIMEText(html_template, "html", "utf-8"))

            # Adjuntar archivos si los hay
            if attachments:
                for file_path in attachments:
                    with open(file_path, "rb") as attachment:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        file_name = os.path.basename(file_path).encode("utf-8").decode("utf-8")
                        part.add_header(
                            "Content-Disposition",
                            f"attachment; filename={file_name}",
                        )
                        message.attach(part)
            # Configurar conexión SMTP según el puerto
            if self.smtp_port == 465:
                with SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                    server.login(self.username, self.password)
                    server.send_message(message)
            elif self.smtp_port == 587:
                with SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls()
                    print(self.username, self.password)
                    server.login(self.username, self.password)
                    server.send_message(message)
            else:
                raise ValueError(f"Puerto no soportado: {self.smtp_port}")

            print(f"Correo enviado exitosamente a {to_email}")

        except Exception as e:
            print(f"Error inesperado: {e}")
