import streamlit as st


# =========================
# MOTOR DE DIAGNÓSTICO - Anamnese do Usuário
# =========================
def diagnostico(respostas):

    problema = respostas["problema"]
    inicio = respostas["inicio"]
    impacto = respostas["impacto"]
    conexao = respostas["conexao"]
    tempo_uso = respostas["tempo_uso"]

    acoes = []
    info_extra = []

    # =========================
    # LENTIDÃO
    # =========================
    if problema == "Lentidão":

        acoes += [
            "🧹 Limpar arquivos temporários do sistema",
            "🌐 Executar flush DNS",
            "🔄 Reiniciar navegador ou sistema"
        ]

        if impacto == "Sistema todo lento":

            acoes += [
                "🛠 Executar SFC /scannow",
                "🧩 Executar DISM RestoreHealth",
                "💽 Verificar disco (chkdsk /scan)"
            ]

    # =========================
    # INTERNET
    # =========================
    if problema == "Internet":

        acoes += [
            "🌐 Reset de rede (Winsock)",
            "🔄 Renovar IP",
            "🧠 Flush DNS"
        ]

    # =========================
    # TRAVAMENTOS
    # =========================
    if problema == "Travamentos":

        acoes += [
            "🛠 Executar SFC /scannow",
            "🧩 Executar DISM RestoreHealth",
            "💽 Verificar disco",
            "🧠 Verificar uso de memória (RAM)"
        ]

    # =========================
    # INÍCIO DO PROBLEMA
    # =========================
    if inicio == "Após atualização recente":

        acoes.append(
            "🔄 Restaurar estabilidade do sistema (SFC + DISM)"
        )

    # =========================
    # CONEXÃO
    # =========================
    if conexao == "Wi-Fi instável":

        acoes.append(
            "📡 Reiniciar roteador/modem"
        )

    # =========================
    # TEMPO SEM REINICIAR
    # =========================
    if tempo_uso == "Mais de 3 dias":

        acoes.insert(
            0,
            "🔄 REINICIAR O COMPUTADOR (alta prioridade)"
        )

        info_extra.append("""
🔄 IMPORTANTE:

REINICIAR NÃO é o mesmo que desligar e ligar.

• REINICIAR:
  - Reinicia completamente o Windows
  - Reinicia serviços do sistema
  - Limpa memória (RAM)
  - Resolve travamentos e lentidão

• DESLIGAR/LIGAR:
  - Pode usar "Inicialização Rápida (Fast Startup)"
  - Parte do sistema pode ser restaurada de estado salvo
  - Nem sempre limpa processos travados

💡 Para diagnóstico técnico, REINICIAR é mais eficaz.
""")

    elif tempo_uso == "1 a 3 dias" and problema == "Lentidão":

        info_extra.append(
            "💡 Recomenda-se reiniciar o sistema para liberar memória acumulada."
        )

    return acoes, info_extra


# =========================
# INTERFACE STREAMLIT
# =========================
def app():

    st.title("🧠 Diagnóstico Guiado do Sistema")

    st.write(
        "Responda às perguntas abaixo para receber "
        "soluções automáticas e orientadas."
    )

    # =========================
    # PERGUNTA 1
    # =========================
    problema = st.selectbox(
        "1️⃣ Qual problema você está enfrentando?",
        [
            "Lentidão",
            "Internet",
            "Travamentos"
        ]
    )

    # =========================
    # PERGUNTA 2
    # =========================
    inicio = st.selectbox(
        "2️⃣ Quando o problema começou?",
        [
            "Hoje / recentemente",
            "Após atualização recente",
            "Não sei"
        ]
    )

    # =========================
    # PERGUNTA 3
    # =========================
    impacto = st.selectbox(
        "3️⃣ O problema afeta:",
        [
            "Apenas um aplicativo",
            "Alguns programas",
            "Sistema todo lento"
        ]
    )

    # =========================
    # PERGUNTA 4
    # =========================
    conexao = st.selectbox(
        "4️⃣ Como está sua conexão de internet?",
        [
            "Normal",
            "Lenta",
            "Wi-Fi instável",
            "Sem internet"
        ]
    )

    # =========================
    # PERGUNTA 5 (NOVA)
    # =========================
    tempo_uso = st.selectbox(
        "5️⃣ Há quanto tempo você não reinicia o computador?",
        [
            "Hoje / recentemente",
            "1 a 3 dias",
            "Mais de 3 dias",
            "Não sei"
        ]
    )

    # =========================
    # EXECUÇÃO
    # =========================
    if st.button("🔎 Gerar diagnóstico"):

        respostas = {
            "problema": problema,
            "inicio": inicio,
            "impacto": impacto,
            "conexao": conexao,
            "tempo_uso": tempo_uso
        }

        acoes, info_extra = diagnostico(respostas)

        st.subheader("💡 Ações recomendadas:")

        for acao in acoes:
            st.write(acao)

        if info_extra:

            st.subheader("ℹ️ Informações importantes:")

            for info in info_extra:
                st.info(info)


# =========================
# EXECUÇÃO
# =========================
if __name__ == "__main__":
    app()
