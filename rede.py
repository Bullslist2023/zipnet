# rede.py

import subprocess
import ctypes


# =========================
# VERIFICA ADMIN
# =========================
def is_admin():

    try:
        return ctypes.windll.shell32.IsUserAnAdmin()

    except Exception:
        return False


# =========================
# EXECUTAR COMANDO
# =========================
def executar(comando):

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
# FLUSH DNS
# =========================
def flush_dns():

    return executar(
        "ipconfig /flushdns"
    )


# =========================
# RENOVAR IP
# =========================
def renew_ip():

    if not is_admin():

        return {
            "sucesso": False,
            "erro": (
                "Execute o programa como administrador"
            )
        }

    comando = (
        "ipconfig /release && "
        "timeout /t 3 > nul && "
        "ipconfig /renew"
    )

    return executar(comando)


# =========================
# PING
# =========================
def ping(host="google.com"):

    return executar(
        f"ping {host} -n 4"
    )


# =========================
# RESET REDE
# =========================
def reset_rede():

    if not is_admin():

        return {
            "sucesso": False,
            "erro": (
                "Execute o programa como administrador"
            )
        }

    comando = (
        "netsh winsock reset && "
        "netsh int ip reset && "
        "ipconfig /flushdns"
    )

    return executar(comando)


# =========================
# TESTE DIRETO
# =========================
if __name__ == "__main__":

    print("=== FLUSH DNS ===")
    print(flush_dns())

    print("\n=== RENEW IP ===")
    print(renew_ip())

    print("\n=== PING ===")
    print(ping())

    print("\n=== RESET REDE ===")
    print(reset_rede())
