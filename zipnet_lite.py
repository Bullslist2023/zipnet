# Projeto do zipnet - Versão Lite
# Esta versão é básica. Apenas versão de aprendizado. Mas que ajudará a resolução de problemas básicos de usuários.
# Versão final em Abril
# Sistema de Soluções ao Usuário
# ========

# Importações das bibliotecas
import os
import streamlit as st # #importando streamlit com apelido para simplificar a chamada
import shutil # P/ manipulação de pastas
import tempfile # P/ arquivo temporário
import subprocess # P/ comando do sistema
import time # Pausa e tempo
import pathlib # Caminhos modernos

# Organizando o esqueleto do app
# Organizando o esqueleto do app
import streamlit as st

from utils import log, executar_com_progresso

from rede import flush_dns, renew_ip, ping
from sistema import get_windows_info
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
            resultado = func()  # 👈 agora captura retorno da função

            st.success(f"{label} concluído!")

            if resultado:
                st.info(resultado)  # 👈 mostra resposta (erro ou sucesso)

    if tipo in ["green", "yellow"]:
        st.markdown('</div>', unsafe_allow_html=True)

# ABAS
abas = st.tabs([
    "📘 Como funciona",
    "🧹 Limpeza",
    "🌐 Rede",
    "🧪 Diagnóstico",
    "⚙️ Avançado"
])

# =====================
# COMO FUNCIONA
# st.write escreve textos e st.info escreve textos em formatos
# =====================
with abas[0]:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.info("Use os botões para executar ações de manutenção no seu computador.")
    st.info("O ZIPNET - Sistema de Suporte ao Usuário (SSU) é um projeto responsável pelo auxílio a pessoas com conhecimento básico em Informática!")
    st.info("Suas funções incluem Auxílio que ajudam desde o básico em desempenho de máquina através de: Limpeza de Arquivos Temporários, Logs, e Lixeira á Ajustes de conexão a Rede Internet com Reinício de Cache DNS, e até mesmo Manutenção avançada usando comandos DISM. Para quem deseja ir mais além, também oferecemos auxílio com verificação de informações simples de configuração de Hardware ao usuário!")
    st.info("O projeto atualmente encontra-se em estado Alfa (Testes Internos), é um desenvolvimento responsável com único intuito de ajudar as pessoas a solucionarem seus problemas diários, oferecendo otimização e solução prático em minutos de uso!!")
    st.markdown('</div>', unsafe_allow_html=True)

# =====================
# LIMPEZA
# =====================
with abas[1]:
    st.markdown('<div class="section">', unsafe_allow_html=True)

    st.subheader("🧹 Limpeza do Sistema")
    st.write("Remova arquivos desnecessários e melhore o desempenho.")

    col1, col2 = st.columns(2)

    with col1:
        botao("🗑 Limpar TEMP", limpar_temp, "green")
        botao("📄 Limpar Logs", limpar_logs)

    with col2:
        botao("🧹 Limpar Cache", limpar_cache)
        botao("⚡ Limpar Prefetch", limpar_prefetch)

    st.write("---")

    botao("🚀 Limpeza Completa", limpeza_completa, "green")

    st.info("A sessão Limpeza é responsável por realizar remoções de arquivos temporários, reduzindo a carga desnecessária, ajudando no tempo de resposta geral e na busca de arquivos!")
    st.info("Os arquivos Cache ou Temporários podem ser causadores de Travamentos, Lentidões em programas ou portais Web, e até mesmo Bugs. ")
    st.info("Realizando essas remoções, podem resolver problemas de bugs em portais Web e correções em erros de carregamentos. Auxiliando em ocasiões onde o ocorre lentidões sem motivos claros.")


    st.markdown('</div>', unsafe_allow_html=True)

# =====================
# REDE
# =====================
with abas[2]:
    st.markdown('<div class="section">', unsafe_allow_html=True)

    st.subheader("🌐 Rede")
    st.write("Corrija problemas de conexão.")

    col1, col2 = st.columns(2)

    with col1:
        botao("🌐 Flush DNS", flush_dns, "yellow")

    with col2:
        botao("🔄 Renovar IP", renew_ip, "yellow")

    st.info("A sessão de ajustes de Rede realiza ações através de correções em DNS e Renovação de IP (Recomendado para quem utiliza conexão DHCP - IPs distribuidos de forma automática pelo provedor de Rede Internet")
    st.info("O DNS funciona como uma agenda em seu computador, se o DNS estiver desatualizado ou apontando para um servidor ruim, os sites podem ficar mais lentos ou não carregar. Então, a ação de limpeza, força a realização de uma nova consulta DNS, agora mais rápida e correta!")
    st.info("Por sua vez, a Renovação de IP resolve conflitos causados por dois dispositivos na mesma rede usando o mesmo IP, assim causando lentidão de internet, ou mesmo quedas de conexão. Ideal para que utiliza conexão DHCP, onde o provedor distribui IPs aos dispositivos automaticamente. Falhas: Conectado sem Internet e Rede instável são corrigidas.")
    st.info("Dentre este cenário, esta sessão resolve problemas de Comunicação com a Internet!")

    st.markdown('</div>', unsafe_allow_html=True)

# =====================
# DIAGNÓSTICO
# =====================
with abas[3]:
    st.markdown('<div class="section">', unsafe_allow_html=True)

    st.subheader("🧪 Diagnóstico do Sistema - Informações Básicas de seu Computador")

    # 🔥 pega dados do sistema
    info = get_windows_info()

    # 🔍 DEBUG VISUAL (ESSENCIAL)
    st.write("📦 Dados brutos retornados:")
    st.json(info)

    st.write("---")

    # 🧠 caso não seja dict, evita quebra
    if not isinstance(info, dict):
        st.error("Erro: get_windows_info() não está retornando um dicionário válido.")
        st.write(info)

    else:
        # 🖥️ SISTEMA
        st.markdown("### 🖥️ Sistema Operacional")

        st.success(f"Sistema: {info.get('sistema', 'N/A')}")
        st.info(f"Edição do Sistema Operacional: {info.get('edicao_windows', 'N/A')}")
        st.info(f"Versão: {info.get('versao', 'N/A')}")
        st.warning(f"Release: {info.get('release', 'N/A')}")

        st.write("---")

        # ⚙️ HARDWARE
        st.markdown("### ⚙️ Hardware")

        st.success(f"Arquitetura: {info.get('arquitetura', 'N/A')}")
        st.info(f"Processador: {info.get('processador', 'N/A')}")
        ram = info.get("ram_total_gb", "N/A")
        st.success(f"RAM Total da Máquina: {ram} GB")


    st.markdown('</div>', unsafe_allow_html=True)
# =====================
# AVANÇADO
# =====================
with abas[4]:
    st.markdown('<div class="section">', unsafe_allow_html=True)

    st.subheader("⚙️ Avançado")

    col1, col2 = st.columns(2)

    with col1:
        botao("🔧 Rodar SFC", sfc)

    with col2:
        botao("🛠 Rodar DISM", dism)

    st.info("Nesta sessão de conteúdos Avançados temos as ações SFC e DISM, ambas são ferramentas nativas do Windows para reparação do Sistema Operacional.")
    st.info("Enquanto o SFC verifica arquivos essenciais do Windows, detecta Corrupção ou alterações e substitui automaticamente por versões corretas. O DISM repara a imagem do Windows, baixa arquivos corretos da Internet (Ou usa a mídia de instalação local) e permite que o SFC funcione corretamente depois.")
    st.info("Por fim, o comando DISM conserta a fonte dos arquivos e o SFC conserta os arquivos em uso. Juntos restauram o sistema operacional para um estado saudável! Use apenas em casos emergentes, a ordem de uso é a ferramenta DISM em primeiro e o SFC por último.")
    st.info("Impacta na estabilidade do sistema, tempo de resposta, travamentos e bugs, e em alguns casos na inicialização do sistema operacional!")

    st.markdown('</div>', unsafe_allow_html=True)

# RODAPÉ
st.markdown("""
<div class="footer">
    <h3>⚡ ZIPNET - SISTEMA DE SUPORTE AO USUÁRIO</h3>
    <p>Seu assistente de manutenção. Garanta a sua Tranquilidade, Performance, e Segurança Digital Básica com poucos passos!</p>
</div>
    <p>Envie o Feedback de sua experiência para contato (E-mail): juansantos227@outlook.com</p>
</div>
""", unsafe_allow_html=True)
