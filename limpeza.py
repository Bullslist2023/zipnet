import os
import shutil
import tempfile
import logging
import platform
from pathlib import Path

# =========================
# CONFIG LOGS
# =========================
logging.basicConfig(
    filename="limpeza.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# =========================
# EXTENSÕES SEGURAS
# =========================
EXTENSOES_SEGURAS = {
    ".tmp",
    ".temp",
    ".log",
    ".cache",
    ".old",
    ".bak",
    ".dmp"
}

# =========================
# VERIFICAÇÃO DE SISTEMA
# =========================
def is_windows():
    return platform.system() == "Windows"


# =========================
# FUNÇÃO BASE SEGURA
# =========================
def limpar_pasta(caminho: Path, filtro_extensao=None):
    if not caminho.exists():
        return 0, 0

    arquivos_removidos = 0
    espaco_liberado = 0

    try:
        itens = list(caminho.iterdir())
    except Exception as e:
        logging.error(f"Erro ao acessar pasta {caminho}: {e}")
        return 0, 0

    for item in itens:

        try:

            # =========================
            # ARQUIVOS
            # =========================
            if item.is_file():

                extensao = item.suffix.lower()

                extensoes_permitidas = (
                    filtro_extensao
                    if filtro_extensao
                    else EXTENSOES_SEGURAS
                )

                if extensao not in extensoes_permitidas:
                    continue

                tamanho = item.stat().st_size

                item.unlink()

                arquivos_removidos += 1
                espaco_liberado += tamanho

            # =========================
            # PASTAS
            # =========================
            elif item.is_dir():

                arquivos_validos = [
                    f for f in item.rglob("*")
                    if (
                        f.is_file()
                        and f.suffix.lower() in EXTENSOES_SEGURAS
                    )
                ]

                tamanho = sum(
                    f.stat().st_size
                    for f in arquivos_validos
                )

                # Remove apenas arquivos seguros
                for arquivo in arquivos_validos:
                    try:
                        arquivo.unlink()
                        arquivos_removidos += 1
                    except Exception as e:
                        logging.error(
                            f"Erro ao remover arquivo {arquivo}: {e}"
                        )

                # Remove pasta vazia
                try:
                    if not any(item.iterdir()):
                        item.rmdir()
                except:
                    pass

                espaco_liberado += tamanho

        except Exception as e:
            logging.error(f"Erro ao processar {item}: {e}")

    return arquivos_removidos, espaco_liberado


# =========================
# LIMPAR TEMP
# =========================
def limpar_temp():

    temp_dir = Path(tempfile.gettempdir())

    arquivos, espaco = limpar_pasta(temp_dir)

    return (
        f"🧹 TEMP: "
        f"{arquivos} arquivos removidos "
        f"({espaco / (1024 ** 2):.2f} MB)"
    )


# =========================
# LIMPAR CACHE
# =========================
def limpar_cache():

    if not is_windows():
        return "❌ Disponível apenas no Windows"

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

    return (
        f"🧹 CACHE: "
        f"{total_arquivos} arquivos removidos "
        f"({total_espaco / (1024 ** 2):.2f} MB)"
    )


# =========================
# LIMPAR LOGS
# =========================
def limpar_logs():

    caminhos = [
        Path(tempfile.gettempdir())
    ]

    if is_windows():
        caminhos.append(Path("C:/Windows/Logs"))

    total_arquivos = 0
    total_espaco = 0

    for caminho in caminhos:

        arquivos, espaco = limpar_pasta(
            caminho,
            filtro_extensao={".log", ".txt"}
        )

        total_arquivos += arquivos
        total_espaco += espaco

    return (
        f"📄 LOGS: "
        f"{total_arquivos} arquivos removidos "
        f"({total_espaco / (1024 ** 2):.2f} MB)"
    )


# =========================
# LIMPAR PREFETCH
# =========================
def limpar_prefetch():

    if not is_windows():
        return "❌ Disponível apenas no Windows"

    prefetch_path = Path("C:/Windows/Prefetch")

    if not prefetch_path.exists():
        return "❌ Pasta Prefetch não encontrada"

    if not os.access(prefetch_path, os.W_OK):
        return "❌ Sem permissão para limpar Prefetch"

    arquivos_removidos = 0

    try:

        for item in prefetch_path.iterdir():

            try:

                if (
                    item.is_file()
                    and item.suffix.lower() == ".pf"
                ):
                    item.unlink()
                    arquivos_removidos += 1

            except Exception as e:
                logging.error(
                    f"Erro ao remover Prefetch {item}: {e}"
                )

    except Exception as e:
        logging.error(f"Erro no Prefetch: {e}")

    return f"⚡ PREFETCH: {arquivos_removidos} arquivos removidos"


# =========================
# LIMPAR LIXEIRA
# =========================
def limpar_lixeira():

    if not is_windows():
        return "❌ Disponível apenas no Windows"

    try:

        comando = (
            "powershell -Command "
            "Clear-RecycleBin -Force "
            "-ErrorAction SilentlyContinue"
        )

        resultado = os.system(comando)

        if resultado == 0:
            return "🗑 Lixeira esvaziada"

        return "❌ Falha ao limpar lixeira"

    except Exception as e:

        logging.error(f"Erro ao limpar lixeira: {e}")

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

        try:

            resultado = etapa()

            resultados.append(resultado)

        except Exception as e:

            logging.error(
                f"Erro na etapa {etapa.__name__}: {e}"
            )

            resultados.append(
                f"❌ Erro em {etapa.__name__}"
            )

    return "\n".join(resultados)
