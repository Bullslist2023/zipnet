import platform

def get_windows_info():
    sistema = platform.system()

    info = {
        "sistema": sistema,
        "arquitetura": platform.machine(),
        "processador": platform.processor()
    }

    if sistema != "Windows":
        info["mensagem"] = "Informações avançadas disponíveis apenas no Windows"
        return info

    try:
        import psutil
        info["ram_total_gb"] = round(psutil.virtual_memory().total / (1024**3), 2)
    except:
        info["ram_total_gb"] = "N/A"

    return info
