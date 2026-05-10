# Projeto do zipnet - Versão Lite
# Esta versão é básica. Apenas versão de aprendizado. Mas que ajudará a resolução de problemas básicos de usuários.
# Versão final em Abril
# Sistema de Soluções ao Usuário
# ========

# Importações das bibliotecas
import os
import streamlit as st  # importando streamlit com apelido para simplificar a chamada
import shutil  # P/ manipulação de pastas
import tempfile  # P/ arquivo temporário
import subprocess  # P/ comando do sistema
import time  # Pausa e tempo
import pathlib  # Caminhos modernos

# Organizando o esqueleto do app
import streamlit as st

from utils import log, executar_com_progresso

from rede import flush_dns, renew_ip, ping
#from sistema import get_windows_info
from avancado import sfc, dism
from styles import load_css

from limpeza import (
    limpar_temp,
    limpar_cache,
    limpar_logs,
    limpar_prefetch,
    limpar_lixeira,
    limpeza_completa
)

# CONFIG
st.set_page_config(page_title="ZIPNET - SISTEMA DE SUPORTE AO USUÁRIO", layout="wide")

# CSS
st.markdown(load_css(), unsafe_allow_html=True)

# TÍTULO
st.markdown('<div class="main-title">💻 ZIPNET - SISTEMA DE SUPORTE AO USUÁRIO</div>', unsafe_allow_html=True)

# Estado
if "logs" not in st.session_state:
    st.session_state.logs = []

# Função padrão de botão
def botao(label, func, tipo="default"):
    if tipo == "green":
        st.markdown('<div class="btn-green">', unsafe_allow_html=True)
    elif tipo == "yellow":
        st.markdown('<div class="btn-yellow">', unsafe_allow_html=True)

    if st.button(label):
        with st.spinner("Executando..."):
            resultado = func()

            st.success(f"{label} concluído!")

            if resultado:
                st.info(resultado)

    if tipo in ["green", "yellow"]:
        st.markdown('</div>', unsafe_allow_html=True)

# ABAS
abas = st.tabs([
    "📘 Como funciona",
    "🧠 Anamnese Guiada",
    "🧹 Limpeza",
    "🌐 Rede",
    "⚙️ Avançado"
])

# =====================
# COMO FUNCIONA
# =====================
with abas[0]:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.info("🫱🏻‍🫲🏽 Use os botões para executar ações de manutenção no seu computador.")
    st.info("🌎 O ZIPNET - Sistema de Suporte ao Usuário (SSU) é um projeto responsável pelo auxílio a pessoas com conhecimento básico em Informática!")
    st.info("💾 Suas funções incluem Auxílio que ajudam desde o básico em desempenho de máquina através de: Limpeza de Arquivos Temporários, Logs, e Lixeira á Ajustes de conexão a Rede Internet com Reinício de Cache DNS, e até mesmo Manutenção avançada usando comandos DISM.")
    st.info("🤔Comece utilizando nosso auxilio de Anamnese Guiada, afim de receber orientações básicas e então partimos para tratativa de seu problema!")
    st.info("🏢O projeto atualmente encontra-se em estado Alfa (Testes Internos), é um desenvolvimento responsável com único intuito de ajudar as pessoas a solucionarem seus problemas diários, oferecendo otimização e solução prático em minutos de uso!!")
    st.markdown('</div>', unsafe_allow_html=True)

# =====================
# DIAGNÓSTICO GUIADO (NOVA ABA PRINCIPAL)
# =====================
with abas[1]:
    st.markdown('<div class="section">', unsafe_allow_html=True)

    st.subheader("🧪 Anamnese Guiada")

    st.write("Responda às perguntas para receber recomendações automáticas.")

    problema = st.selectbox(
        "1️⃣ Qual problema você está enfrentando?",
        ["Lentidão", "Internet", "Travamentos"]
    )

    inicio = st.selectbox(
        "2️⃣ Quando o problema começou?",
        ["Hoje / recentemente", "Após atualização recente", "Não sei"]
    )

    impacto = st.selectbox(
        "3️⃣ O problema afeta:",
        ["Apenas um aplicativo", "Alguns programas", "Sistema todo lento"]
    )

    conexao = st.selectbox(
        "4️⃣ Sua conexão de internet:",
        ["Normal", "Lenta", "Wi-Fi instável", "Sem internet"]
    )

    tempo_uso = st.selectbox(
        "5️⃣ Há quanto tempo você não reinicia o computador?",
        ["Hoje / recentemente", "1 a 3 dias", "Mais de 3 dias", "Não sei"]
    )

    if st.button("🔎 Gerar diagnóstico"):

        acoes = []

        if problema == "Lentidão":
            acoes += [
                "🧹 Limpar arquivos temporários",
                "🌐 Flush DNS",
                "🔄 Reiniciar sistema"
            ]

            if impacto == "Sistema todo lento":
                acoes += [
                    "🛠 SFC /scannow",
                    "🧩 DISM RestoreHealth"
                ]

        if problema == "Internet":
            acoes += [
                "🌐 Reset de rede",
                "🔄 Renovar IP",
                "🧠 Flush DNS"
            ]

        if tempo_uso == "Mais de 3 dias":

            st.warning("🔄 Recomendação importante")

            st.info("""
🔄 REINICIAR é diferente de desligar.

• REINICIAR:
- Reinicia o Windows completamente
- Limpa memória RAM
- Reinicia serviços do sistema

• DESLIGAR/LIGAR:
- Pode usar Inicialização Rápida (Fast Startup)
- Nem sempre limpa processos travados

💡 Para lentidão e erros, reiniciar é mais eficaz.
""")

            acoes.insert(0, "🔄 Reiniciar o computador (alta prioridade)")

        st.subheader("💡 Ações recomendadas:")

        for acao in acoes:
            st.write(acao)

    st.markdown('</div>', unsafe_allow_html=True)

# =====================
# LIMPEZA
# =====================
with abas[2]:
    st.markdown('<div class="section">', unsafe_allow_html=True)

    st.subheader("🧹 Limpeza do Sistema")

    col1, col2 = st.columns(2)

    with col1:
        botao("🗑 Limpar TEMP", limpar_temp, "green")
        botao("📄 Limpar Logs", limpar_logs)

    with col2:
        botao("🧹 Limpar Cache", limpar_cache)
        botao("⚡ Limpar Prefetch", limpar_prefetch)

    botao("🚀 Limpeza Completa", limpeza_completa, "green")

    st.markdown('</div>', unsafe_allow_html=True)

# =====================
# REDE
# =====================
with abas[3]:
    st.markdown('<div class="section">', unsafe_allow_html=True)

    st.subheader("🌐 Rede")

    col1, col2 = st.columns(2)

    with col1:
        botao("🌐 Flush DNS", flush_dns, "yellow")

    with col2:
        botao("🔄 Renovar IP", renew_ip, "yellow")

    st.markdown('</div>', unsafe_allow_html=True)

# =====================
# AVANÇADO
# =====================
with abas[4]:
    st.markdown('<div class="section">', unsafe_allow_html=True)

    st.subheader("⚙️ Avançado")

    col1, col2 = st.columns(2)

    with col1:
        botao("🔧Verificar possíveis arquivos corrompidos e substituir automaticamente (DISM)", sfc)

    with col2:
        botao("🛠 Corrigir Imagem do Windows (DISM)", dism)
        
    st.info("O que é IMAGEM do WIndows? Pense como uma Foto do estado atual do Sistema Operacional.")
    st.info("Em caso de urgência, você pode formatar seu computador usando esta imagem exatamente o estado em que está, com seus arquivos de fotos, vídeos, programas, etc.")
    st.info("Modo de uso: Use o DISM primeiro, para garantir que a fonte de reparo esteja boa, e o SFC posteriormente para aplicar o conserto dos arquivos!")
    st.info("Quando usar: Janelas travando ou fechando sozinha. Mensagem de erro de arquivos (.dll ausente). Menu Iniciar ou Barra de Tarefas não respondem. Erro de atualização do Windows. Infecção de Vírus. Até mesmo em Tela Azul BSOD.")
    st.markdown('</div>', unsafe_allow_html=True)

# =====================
# RODAPÉ
# =====================
st.markdown("""
<div class="footer">
    <h3>⚡ ZIPNET - SISTEMA DE SUPORTE AO USUÁRIO</h3>
    <p>Seu assistente de manutenção.</p>
</div>
""", unsafe_allow_html=True)
