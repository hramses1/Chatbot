from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta, time
import pickle
import os
from google.auth.transport.requests import Request

# Configuración de los permisos de Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = './src/feature/chatbot/utils/credentials.json'

def get_calendar_service():
    creds = None
    token_path = './src/feature/chatbot/utils/token.pickle'
    
    # Cargar token si existe
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    
    # Si no hay credenciales válidas, solicita autenticación
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Guarda las credenciales para futuras ejecuciones
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    
    service = build('calendar', 'v3', credentials=creds)
    return service

def listar_calendarios():
    service = get_calendar_service()
    calendars_result = service.calendarList().list().execute()
    calendars = calendars_result.get('items', [])
    
    print("Calendarios disponibles:")
    for calendar in calendars:
        print(f"- {calendar['summary']} (ID: {calendar['id']})")
    return calendars

def is_within_working_hours(dt, start_time, end_time):
    current_time = dt.time()
    return start_time <= current_time < end_time

def verificar_disponibilidad(service, calendar_ids, time_min, time_max):
    body = {
        "timeMin": time_min,
        "timeMax": time_max,
        "timeZone": "America/Guayaquil",
        "items": [{"id": calendar_id} for calendar_id in calendar_ids]
    }
    
    response = service.freebusy().query(body=body).execute()
    busy_times = []
    for calendar_id in calendar_ids:
        status = response['calendars'][calendar_id].get('errors', [])
        if status:
            print(f"Error al acceder al calendario {calendar_id}: {status}")
        else:
            busy_times.extend(response['calendars'][calendar_id].get('busy', []))
    return busy_times

def crear_evento_google_calendar(cliente_nombre, cliente_email, abogado_email, fecha, hora_inicio, duracion_minutos=20):
    service = get_calendar_service()
    
    # Calendarios a verificar
    calendar_ids = ['estudiojuridicocamachogomez@gmail.com', abogado_email]
    
    # Definir horario de atención
    hora_apertura = time(8, 0)   # 8:00 AM
    hora_cierre = time(17, 0)    # 5:00 PM
    max_dias_busqueda = 7        # Número máximo de días para buscar disponibilidad
    dias_busqueda = 0            # Contador de días buscados
    
    # Convertir fecha y hora de inicio a objeto datetime
    zona_horaria = "-05:00"  # Ajusta la zona horaria según corresponda
    formato_fecha_hora = "%Y-%m-%dT%H:%M:%S%z"
    fecha_hora_inicio_str = f"{fecha}T{hora_inicio}:00{zona_horaria}"
    try:
        inicio_datetime = datetime.strptime(fecha_hora_inicio_str, formato_fecha_hora)
    except ValueError as ve:
        print(f"Error en el formato de fecha y hora: {ve}")
        return
    
    duracion = timedelta(minutes=duracion_minutos)
    fin_datetime = inicio_datetime + duracion
    
    while dias_busqueda <= max_dias_busqueda:
        # Verificar si el horario está dentro del horario de atención
        if (is_within_working_hours(inicio_datetime, hora_apertura, hora_cierre) and
            is_within_working_hours(fin_datetime, hora_apertura, hora_cierre) and
            inicio_datetime.date() == fin_datetime.date()):
            
            time_min = inicio_datetime.isoformat()
            time_max = fin_datetime.isoformat()
            
            try:
                print("\nVerificando disponibilidad en los calendarios...")
                print(f"Fecha y hora de inicio: {inicio_datetime.strftime('%Y-%m-%d %H:%M')}")
                print(f"Fecha y hora de fin: {fin_datetime.strftime('%Y-%m-%d %H:%M')}")
                
                busy_times = verificar_disponibilidad(service, calendar_ids, time_min, time_max)
                
                if busy_times:
                    print("\nConflictos encontrados:")
                    for busy in busy_times:
                        print(f"- Ocupado desde {busy['start']} hasta {busy['end']}")
                    
                    # Incrementar el tiempo en la duración de la reunión
                    inicio_datetime += duracion
                    fin_datetime += duracion
                else:
                    # No hay conflictos, crear el evento
                    print("No hay conflictos, creando evento...")
                    event = {
                        'summary': f'Cita con {cliente_nombre}',
                        'location': 'Oficina del Estudio Jurídico',
                        'description': 'Reunión de asesoramiento legal con el abogado.',
                        'start': {
                            'dateTime': inicio_datetime.isoformat(),
                            'timeZone': 'America/Guayaquil',
                        },
                        'end': {
                            'dateTime': fin_datetime.isoformat(),
                            'timeZone': 'America/Guayaquil',
                        },
                        'attendees': [
                            {'email': cliente_email},
                            {'email': abogado_email}
                        ],
                        'reminders': {
                            'useDefault': False,
                            'overrides': [
                                {'method': 'email', 'minutes': 24 * 60},
                                {'method': 'popup', 'minutes': 10},
                            ],
                        },
                    }
                    
                    event_result = service.events().insert(
                        calendarId='estudiojuridicocamachogomez@gmail.com',
                        body=event,
                        sendUpdates='all'
                    ).execute()
                    
                    print(f"Evento creado exitosamente: {event_result.get('htmlLink')}")
                    return  # Salir de la función al crear el evento exitosamente
                
            except Exception as e:
                print(f"Error al verificar disponibilidad o crear el evento: {e}")
                return
        else:
            # Si el horario no está dentro del horario de atención, pasar al siguiente intervalo
            inicio_datetime += duracion
            fin_datetime = inicio_datetime + duracion
        
        # Si el fin de la cita supera el horario laboral, pasar al siguiente día laboral
        if fin_datetime.time() > hora_cierre or inicio_datetime.time() < hora_apertura:
            inicio_datetime = inicio_datetime.replace(hour=hora_apertura.hour, minute=hora_apertura.minute, second=0) + timedelta(days=1)
            fin_datetime = inicio_datetime + duracion
            dias_busqueda += 1
            print(f"Cambiando al siguiente día laboral: {inicio_datetime.strftime('%Y-%m-%d')}")
            continue
    
    print("No se encontró disponibilidad en los próximos días.")

# Llamar a la función para listar los calendarios
listar_calendarios()

