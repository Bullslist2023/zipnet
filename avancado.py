# Para verificação de arquivos do SO e Substituição de arquivos corrompidos automaticamente
# Para Checagem de problemas e reparos profundos do Windows
# Para Análise ainda mais profunda no Windows
# Para Correção de Profundos do Windows

import subprocess
import ctypes
import platform


# =========================
# VERIFICA SE É WINDOWS
# =========================
def is_windows():

    return platform.system() == "Windows"


# =========================
# VERIFICA ADMINISTRADOR
# =========================
def is_admin():

    try:
        return ctypes.windll.shell32.IsUserAnAdmin()

    except Exception:
        return False


# =========================
# EXECUTAR COMANDO
# =========================
def executar_comando(comando):

    try:

        resultado = subprocess.run(
            comando,
            shell=True,
            capture_output=True,
            text=True,
            encoding="utf-8"
        )

        return {
            "sucesso": resultado.returncode == 0,
            "codigo": resultado.returncode,
            "saida": resultado.stdout.strip(),
            "erro": resultado.stderr.strip()
        }

    except Exception as e:

        return {
            "sucesso": False,
            "codigo": -1,
            "saida": "",
            "erro": str(e)
        }


# =========================
# SFC
# Verifica arquivos corrompidos
# e substitui automaticamente
# =========================
def sfc():

    if not is_windows():

        return {
            "sucesso": False,
            "erro": "❌ SFC só funciona no Windows"
        }

    if not is_admin():

        return {
            "sucesso": False,
            "erro": (
                "❌ Execute o programa "
                "como administrador"
            )
        }

    return executar_comando(
        "sfc /scannow"
    )


# =========================
# DISM
# Corrige imagem do Windows
# =========================
def dism():

    if not is_windows():

        return {
            "sucesso": False,
            "erro": "❌ DISM só funciona no Windows"
        }

    if not is_admin():

        return {
            "sucesso": False,
            "erro": (
                "❌ Execute o programa "
                "como administrador"
            )
        }

    return executar_comando(
        "DISM /Online /Cleanup-Image /RestoreHealth"
    )


# =========================
# CHECK HEALTH
# Verifica corrupção leve
# sem reparo profundo
# =========================
def check_health():

    if not is_windows():

        return {
            "sucesso": False,
            "erro": (
                "❌ Disponível apenas "
                "no Windows"
            )
        }

    return executar_comando(
        "DISM /Online /Cleanup-Image /CheckHealth"
    )


# =========================
# SCAN HEALTH
# Faz análise profunda
# da imagem do Windows
# =========================
def scan_health():

    if not is_windows():

        return {
            "sucesso": False,
            "erro": (
                "❌ Disponível apenas "
                "no Windows"
            )
        }

    return executar_comando(
        "DISM /Online /Cleanup-Image /ScanHealth"
    )


# =========================
# CHKDSK
# Verifica problemas no disco
# sem reiniciar o sistema
# =========================
def chkdsk():

    if not is_windows():

        return {
            "sucesso": False,
            "erro": (
                "❌ Disponível apenas "
                "no Windows"
            )
        }

    return executar_comando(
        "chkdsk /scan"
    )


# =========================
# REPARO COMPLETO
# Executa sequência automática
# de reparos inteligentes
# =========================
def reparar_windows():

    if not is_windows():

        return {
            "sucesso": False,
            "erro": (
                "❌ Disponível apenas "
                "no Windows"
            )
        }

    if not is_admin():

        return {
            "sucesso": False,
            "erro": (
                "❌ Execute o programa "
                "como administrador"
            )
        }

    etapas = []

    comandos = [

        (
            "🔎 Verificando integridade do Windows...",
            (
                "DISM /Online "
                "/Cleanup-Image "
                "/CheckHealth"
            )
        ),

        (
            "🧠 Fazendo análise profunda...",
            (
                "DISM /Online "
                "/Cleanup-Image "
                "/ScanHealth"
            )
        ),

        (
            "🛠 Corrigindo imagem do Windows...",
            (
                "DISM /Online "
                "/Cleanup-Image "
                "/RestoreHealth"
            )
        ),

        (
            "📦 Corrigindo arquivos corrompidos...",
            "sfc /scannow"
        ),

        (
            "💽 Verificando disco...",
            "chkdsk /scan"
        ),

        (
            "🌐 Reparando rede...",
            (
                "netsh winsock reset && "
                "netsh int ip reset && "
                "ipconfig /flushdns"
            )
        )
    ]

    for descricao, comando in comandos:

        resultado = executar_comando(comando)

        etapas.append({
            "etapa": descricao,
            "resultado": resultado
        })

    return {
        "sucesso": True,
        "reiniciar_recomendado": True,
        "etapas": etapas
    }


# =========================
# TESTE LOCAL
# =========================
if __name__ == "__main__":

    resultado = reparar_windows()

    for etapa in resultado.get("etapas", []):

        print("\n")
        print(etapa["etapa"])

        if etapa["resultado"]["sucesso"]:

            print("✅ Sucesso")

        else:

            print("❌ Falha")

        print(etapa["resultado"]["saida"])
        print(etapa["resultado"]["erro"])
