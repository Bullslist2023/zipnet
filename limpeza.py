import os
import shutil
import tempfile
from pathlib import Path
import platform

# =========================
# VERIFICAÇÃO DE SISTEMA
# =========================
def is_windows():
    return platform.system() == "Windows"


# =========================
# FUNÇÃO BASE
# =========================
def limpar_pasta(caminho: Path, filtro_extensao=None):
    if not caminho.exists():
        return 0, 0

    arquivos_removidos = 0
    espaco_liberado = 0

    for item in caminho.iterdir():
        try:
            if item.is_file():
                if filtro_extensao and item.suffix.lower() not in filtro_extensao:
                    continue
                espaco_liberado += item.stat().st_size
                item.unlink()
                arquivos_removidos += 1

            elif item.is_dir():
                tamanho = sum(
                    f.stat().st_size for f in item.rglob('*') if f.is_file()
                )
                shutil.rmtree(item, ignore_errors=True)
                espaco_liberado += tamanho
                arquivos_removidos += 1

        except:
            continue

    return arquivos_removidos, espaco_liberado


# =========================
# LIMPEZAS
# =========================
def limpar_temp():
    temp_dir = Path(tempfile.gettempdir())
    arquivos, espaco = limpar_pasta(temp_dir)

    return f"🧹 TEMP: {arquivos} arquivos removidos ({espaco / (1024**2):.2f} MB)"


def limpar_cache():
    if not is_windows():
        return "❌ Cache avançado disponível apenas no Windows"

    caminhos = [
        Path.home() / "AppData/Local/Temp",
        Path.home() / "AppData/Local/Microsoft/Windows/INetCache",
    ]

    total_arquivos = 0
    total_espaco = 0

    for caminho in caminhos:
        arquivos, espaco = limpar_pasta(caminho)
        total_arquivos += arquivos
        total_espaco += espaco

    return f"🧹 CACHE: {total_arquivos} arquivos ({total_espaco / (1024**2):.2f} MB)"


def limpar_logs():
    caminhos = [
        Path(tempfile.gettempdir()),
    ]

    if is_windows():
        caminhos.append(Path("C:/Windows/Logs"))

    total_arquivos = 0
    total_espaco = 0

    for caminho in caminhos:
        arquivos, espaco = limpar_pasta(
            caminho, filtro_extensao={".log", ".txt"}
        )
        total_arquivos += arquivos
        total_espaco += espaco

    return f"📄 LOGS: {total_arquivos} arquivos ({total_espaco / (1024**2):.2f} MB)"


def limpar_prefetch():
    if not is_windows():
        return "❌ Prefetch disponível apenas no Windows"

    prefetch_path = Path("C:/Windows/Prefetch")

    arquivos = 0

    for item in prefetch_path.iterdir():
        try:
            if item.is_file() and item.suffix.lower() == ".pf":
                item.unlink()
                arquivos += 1
        except:
            continue

    return f"⚡ PREFETCH: {arquivos} arquivos removidos"


def limpar_lixeira():
    if not is_windows():
        return "❌ Lixeira automática disponível apenas no Windows"

    try:
        os.system("powershell -Command Clear-RecycleBin -Force -ErrorAction SilentlyContinue")
        return "🗑 Lixeira esvaziada"
    except:
        return "❌ Erro ao limpar lixeira"


# =========================
# LIMPEZA COMPLETA
# =========================
def limpeza_completa():
    etapas = [
        limpar_temp,
        limpar_cache,
        limpar_logs,
        limpar_prefetch,
        limpar_lixeira
    ]

    resultados = []

    for etapa in etapas:
        resultado = etapa()
        resultados.append(resultado)

    return "\n".join(resultados)
