import subprocess

def sfc():
    subprocess.run(["sfc", "/scannow"]) # Para verificação de arquivos do SO e Substituição de arquivos corrompidos automaticamente

def dism():
    subprocess.run(["DISM", "/Online", "Cleanup-Image", "/CheckHealth"]) # Para Checagem de problemas e reparos profundos do Windows

def dism():
    subprocess.run(["DISM", "/Online", "Cleanup-Image", "ScanHealth"]) # Para Análise ainda mais profunda no Windows
def dism():
    subprocess.run(["DISM", "/Online", "/Cleanup-Image", "/RestoreHealth"]) # Para Correção de Profundos do Windows