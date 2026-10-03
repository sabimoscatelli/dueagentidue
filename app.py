import streamlit as st
from openai import OpenAI

# Configurazione della pagina
st.set_page_config(page_title="Team Didattica IA - Esame PET", page_icon="🎓")
st.title("🎓 Team Didattica ESL & IA - Preparazione PET")
st.write("Seleziona con quale agente vuoi parlare!")

# Recupera la chiave segreta dalla cassaforte di Streamlit
if "OPENAI_API_KEY" not in st.secrets:
    st.error("⚠️ Manca la chiave API. Vai nei Settings di Streamlit -> Secrets e aggiungi OPENAI_API_KEY.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 1. IL SELETTORE DEGLI AGENTI
agente_scelto = st.radio(
    "Chi vuoi attivare?",
    ("💡 Agente 1: Cerca attività pratiche PET", "📝 Agente 2: Scrivi la newsletter")
)

# 2. LE PERSONALITÀ DEGLI AGENTI (I Prompt di Sistema aggiornati)
istruzioni_agente_1 = """Sei un esperto di didattica delle lingue straniere (ESL) e intelligenza artificiale. 
Ispirandoti a fonti autorevoli come Eric Curts, Dan Fitzpatrick e Maestro Roberto, il tuo compito è proporre ESATTAMENTE 5 attività pratiche, pronte all'uso e rapidamente declinabili in classe.
Ogni attività deve includere l'utilizzo di un piccolo strumento o funzione di IA.

Il tuo target:
- Studenti: 14-16 anni.
- Livello: B1 (Preparazione Esame PET - Preliminary English Test).
- Gli argomenti (topics) devono essere adatti alla loro età e utili per il PET (es. hobby, tecnologia, ambiente, viaggi, vita scolastica).

Per ogni idea, fornisci:
- Fonte dalla quale hai preso l'idea.
- Titolo accattivante.
- Topic affrontato (utile per il PET).
- Strumento IA suggerito (es. ChatGPT, un generatore di immagini, un correttore, ecc.).
- Cosa fanno gli studenti (in 2 righe, in modo molto pratico e operativo).
Sii sintetico, chiaro e orientato all'azione."""

istruzioni_agente_2 = """Sei un redattore divulgativo esperto in didattica dell'inglese (ESL) per la scuola secondaria. L'utente ti indicherà una delle attività pratiche suggerite dall'Agente 1.
Devi scrivere una breve newsletter in italiano che spieghi quell'attività in maniera chiara ai colleghi docenti. 

Struttura la newsletter con: 
- Breve introduzione (perché questa attività funziona per i ragazzi di 14-16 anni che preparano il PET).
- Fornisci sempre 12 items lessicali (verbi, idioms e aggettivi) che servano agli studenti per consolidare questo topic
- Fornisci sempre anche 5 sostantivi
- Vantaggi e svantaggi dell'uso dell'IA in questo specifico caso.
- Modalità d'uso in classe (passo-passo, in modo molto pratico).
- Spiega come si svolgerà l'attività (chi fa cosa)
- Spiega perche' l'attivita' viene bene con l'AI
- Consigli e raccomandazioni (come evitare che i ragazzi "copino", come gestire eventuali difficoltà tecniche). 

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
    else:
        istruzioni = istruzioni_agente_2

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
                model="gpt-3.5-turbo",
                messages=messaggi_per_ia
            )
            testo_definitivo = risposta_ia.choices[0].message.content
            
            # Mostra la risposta a schermo e salvala in memoria
            risposta_temporanea.markdown(testo_definitivo)
            st.session_state.messaggi.append({"role": "assistant", "content": testo_definitivo})
            
        except Exception as e:
            risposta_temporanea.error("Oops! Controlla di aver inserito correttamente l'API Key nei Secrets e di avere credito in OpenAI.")
