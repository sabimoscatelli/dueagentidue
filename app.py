import streamlit as st
from openai import OpenAI

# Configurazione della pagina
st.set_page_config(page_title="Team Didattica IA", page_icon="🎓")
st.title("🎓 Team Didattica ESL & IA")
st.write("Seleziona con quale agente vuoi parlare!")

# Recupera la chiave segreta dalla cassaforte di Streamlit
if "OPENAI_API_KEY" not in st.secrets:
    st.error("⚠️ Manca la chiave API. Vai nei Settings di Streamlit -> Secrets e aggiungi OPENAI_API_KEY.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 1. IL SELETTORE DEGLI AGENTI
agente_scelto = st.radio(
    "Chi vuoi attivare?",
    ("💡 Agente 1: Cerca Idee", "📝 Agente 2: Scrivi la newsletter")
)

# 2. LE PERSONALITÀ DEGLI AGENTI (I Prompt di Sistema)
istruzioni_agente_1 = """Sei un esperto di didattica delle lingue straniere (ESL) e intelligenza artificiale. 
Ispirandoti a fonti autorevoli come Eric Curts, Dan Fitzpatrick e Maestro Roberto, il tuo compito è proporre ESATTAMENTE 5 idee pratiche e sintetiche su come usare piccole attività di IA per migliorare l'apprendimento delle lingue da parte di parlanti non nativi. Sii molto breve, schematico e vai dritto al punto."""

istruzioni_agente_2 = """Sei un redattore divulgativo esperto in didattica dell'inglese (ESL). L'utente ti indicherà un'idea o un argomento.
Devi scrivere una breve newsletter in italiano che spieghi l'esempio in maniera chiara. 
Struttura la newsletter con: 
- Breve introduzione
- Vantaggi e svantaggi
- Modalità d'uso in classe, con istruzioni passo passo per il docente, indicando anche il software da utilizzare. La lezione deve essere sempre calibrata su 55 minuti.
- Proposta del lessico necessario in British English, con almeno 12 items suddivisi in aggettivi, avverbi, idioms, verbi e sostantivi
- Consigli e raccomandazioni perche' l'attivita' sia praticabile in classe. 
Il tuo linguaggio deve essere amichevole, rassicurante e adeguato a docenti che si avvicinano per la prima volta all'IA. Non devi MAI disconoscere l'importanza e l'insostituibilità del ruolo del docente umano, anzi devi valorizzarlo."""

# 3. GESTIONE DELLA CHAT
if "messaggi" not in st.session_state:
    st.session_state.messaggi = []

# Mostra i messaggi passati
for msg in st.session_state.messaggi:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Casella di testo per l'utente
prompt_utente = st.chat_input("Scrivi qui la tua richiesta...")

if prompt_utente:
    # Mostra quello che ha scritto l'utente
    st.session_state.messaggi.append({"role": "user", "content": prompt_utente})
    with st.chat_message("user"):
        st.markdown(prompt_utente)

    # Capisce quali istruzioni usare in base all'agente scelto
    if "Agente 1" in agente_scelto:
        istruzioni = istruzioni_agente_1
        nome_agente = "Agente 1"
    else:
        istruzioni = istruzioni_agente_2
        nome_agente = "Agente 2"

    # Prepara i messaggi da mandare al "cervello" dell'IA
    messaggi_per_ia = [{"role": "system", "content": istruzioni}]
    # Aggiunge tutta la conversazione precedente per far ricordare all'IA cosa vi siete detti
    for m in st.session_state.messaggi:
        messaggi_per_ia.append({"role": m["role"], "content": m["content"]})

    # 4. CHIAMATA ALLA VERA IA
    with st.chat_message("assistant"):
        risposta_temporanea = st.empty()
        risposta_temporanea.markdown("Sto pensando... ⏳")
        
        try:
            # Contatta OpenAI
            risposta_ia = client.chat.completions.create(
                model="gpt-3.5-turbo", # Il modello veloce ed economico di OpenAI
                messages=messaggi_per_ia
            )
            testo_definitivo = risposta_ia.choices[0].message.content
            
            # Mostra la risposta a schermo e salvala in memoria
            risposta_temporanea.markdown(testo_definitivo)
            st.session_state.messaggi.append({"role": "assistant", "content": testo_definitivo})
            
        except Exception as e:
            risposta_temporanea.error("Oops! Controlla di aver inserito correttamente l'API Key e di avere credito nel tuo account OpenAI.")
