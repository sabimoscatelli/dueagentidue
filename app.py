import streamlit as st
import time

# Titolo della pagina
st.title("La mia prima Chat Multi-Agente 🤖")
st.write("Scrivi un messaggio e guarda come rispondono Alice e Bob!")

# Inizializza la memoria della chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostra i messaggi passati
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Casella di testo dove l'utente scrive
prompt = st.chat_input("Scrivi qualcosa...")

if prompt:
    # Mostra il messaggio dell'utente
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    time.sleep(0.5) # Pausa per simulare che il bot stia "pensando"

    # Risposta dell'Agente 1 (Alice)
    with st.chat_message("Alice", avatar="👩‍💻"):
        st.markdown(f"Ciao! Sono Alice. Hai scritto: '{prompt}'. Bob, cosa ne pensi?")
    st.session_state.messages.append({"role": "Alice", "content": f"Ciao! Sono Alice. Hai scritto: '{prompt}'. Bob, cosa ne pensi?"})
    
    time.sleep(1) # Un'altra pausa

    # Risposta dell'Agente 2 (Bob)
    with st.chat_message("Bob", avatar="👨‍🔧"):
        st.markdown("Eccomi! Sono Bob. Sono d'accordo con Alice, ottima prova!")
    st.session_state.messages.append({"role": "Bob", "content": "Eccomi! Sono Bob. Sono d'accordo con Alice, ottima prova!"})
