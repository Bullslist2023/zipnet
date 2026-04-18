# Novo código de padronização, evitando a quebra do código em ambiente linux, usado no Streamlit Cloud
# Vamos chammar de system_utils
import platform
import subprocess

def is_windows():
    return platform.system() == "Windows"

def executar_comando(cmd_windows, cmd_linux=None, cmd_mac=None):
    sistema = platform.system()

    try:
        if sistema == "Windows":
            resultado = subprocess.run(cmd_windows, shell=True, capture_output=True, text=True)
        elif sistema == "Linux" and cmd_linux:
            resultado = subprocess.run(cmd_linux, shell=True, capture_output=True, text=True)
        elif sistema == "Darwin" and cmd_mac:
            resultado = subprocess.run(cmd_mac, shell=True, capture_output=True, text=True)
        else:
            return f"❌ Função não suportada no sistema: {sistema}"

        return resultado.stdout if resultado.stdout else "✅ Comando executado"

    except Exception as e:
        return f"❌ Erro: {str(e)}"