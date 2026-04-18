# Para verificação de arquivos do SO e Substituição de arquivos corrompidos automaticamente
# Para Checagem de problemas e reparos profundos do Windows
# Para Análise ainda mais profunda no Windows
# Para Correção de Profundos do Windows

from system_utils import executar_comando, is_windows

def sfc():
    if not is_windows():
        return "❌ SFC só funciona no Windows"

    return executar_comando("sfc /scannow")

def dism():
    if not is_windows():
        return "❌ DISM só funciona no Windows"

    return executar_comando("DISM /Online /Cleanup-Image /RestoreHealth")
