import streamlit as st
import time

def log(msg):
    st.session_state.logs.append(msg)
    st.text("\n".join(st.session_state.logs[-15:]))

def executar_com_progresso(tarefas):
    progresso = st.progress(0)
    total = len(tarefas)

    for i, (msg, func) in enumerate(tarefas):
        log(f"▶ {msg}...")
        try:
            func()
            log(f"✔ {msg} concluído")
        except Exception as e:
            log(f"❌ Erro em {msg}: {e}")

        progresso.progress((i + 1) / total)
        time.sleep(0.3)