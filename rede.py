import subprocess

def flush_dns():
    subprocess.run(["ipconfig", "/flushdns"])

def renew_ip():
    subprocess.run(["ipconfig", "/release"])
    subprocess.run(["ipconfig", "/renew"])

def ping():
    result = subprocess.run(["ping", "-n", "1", "google.com"], capture_output=True, text=True)

    for linha in result.stdout.split("\n"):
        if "tempo=" in linha:
            return linha.split("tempo=")[-1].replace("ms", "").strip()
    return "Erro"