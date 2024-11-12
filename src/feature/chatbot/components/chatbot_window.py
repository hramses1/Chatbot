import streamlit as st

def chat_window(messages):
    """Renderiza los mensajes en la ventana de chat."""
    for message in messages:
        # Verificar si el mensaje es un diccionario con la estructura correcta
        if isinstance(message, dict):
            sender = message.get("sender")
            text = message.get("text", "")

            if sender == "user":
                st.markdown(f"**🧑‍💼 Tú:** {text}")
            elif sender == "bot":
                st.markdown(f"**🤖 Bot:** {text}")
            else:
                st.write(f"🗨️ {text}")
        else:
            # Si no es un diccionario válido, mostrarlo como texto simple
            st.write(f"🗨️ {message}")
