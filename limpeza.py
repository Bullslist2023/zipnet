import tempfile
import shutil
from pathlib import Path

#def limpar_temp():
#    temp_dir = tempfile.gettempdir()
#    print(f'Limpando: {temp_dir}')

#def limpar_cache():
#    print("Limpando Arquivos Cache do Usuário")

#def limpar_logs():
#    print("Limpando Arquivos Logs do Usuário")

#def limpar_lixeira():
#    print("Limpando a Lixeira do Usuário")

#def limpeza_completa():
#    etapas = [
#        limpar_temp,
#        limpar_cache,
#        limpar_logs,
#        limpar_lixeira
#    ]
#    for etapa in etapas:
#        print(f'Executando: {etapa.__name__}') # Este comando possui dois underline antes e depois
#        etapa()

#limpeza_completa()

import os # Para interação com o Windows
import shutil # Edição, Movimentação, Cópia e Exclusão de pastas
import tempfile # Para exclusão de arquivos temporários
from pathlib import Path # Trabalha com Caminhos e pastas
from tqdm import tqdm # Para exibição de uma barra de carregamento

# =========================
# FUNÇÃO BASE (REUTILIZÁVEL)
# =========================
def limpar_pasta(caminho: Path, filtro_extensao=None):
    """
    Limpa uma pasta de forma segura.
    filtro_extensao: lista de extensões para filtrar arquivos (ex: {'.log', '.txt'})
    Retorna quantidade de arquivos removidos e espaço liberado (em bytes)
    """
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
                tamanho = sum(f.stat().st_size for f in item.rglob('*') if f.is_file())
                shutil.rmtree(item, ignore_errors=True)
                espaco_liberado += tamanho
                arquivos_removidos += 1
        except Exception:
            continue

    return arquivos_removidos, espaco_liberado



# =========================
# FUNÇÕES DE LIMPEZA ESPECÍFICAS
# TEMP, CACHE, PREFETCH E LIXEIRA
# =========================
def limpar_temp():
    temp_dir = Path(tempfile.gettempdir())
    print(f"\n[TEMP] Limpando: {temp_dir}")
    return limpar_pasta(temp_dir)

def limpar_cache():
    caminhos = [
        Path.home() / "AppData/Local/Temp",
        Path.home() / "AppData/Local/Microsoft/Windows/INetCache",
    ]
    total_arquivos = 0
    total_espaco = 0
    for caminho in caminhos:
        print(f"\n[CACHE] Limpando: {caminho}")
        arquivos, espaco = limpar_pasta(caminho)
        total_arquivos += arquivos
        total_espaco += espaco
    return total_arquivos, total_espaco

def limpar_logs():
    caminhos = [
        Path("C:/Windows/Logs"),
        Path.home() / "AppData/Local/Temp",
    ]
    total_arquivos = 0
    total_espaco = 0
    for caminho in caminhos:
        print(f"\n[LOGS] Limpando: {caminho}")
        arquivos, espaco = limpar_pasta(caminho, filtro_extensao={".log", ".txt"})
        total_arquivos += arquivos
        total_espaco += espaco
    return total_arquivos, total_espaco


def limpar_prefetch():
    prefetch_path = Path("C:/Windows/Prefetch")
    print("\n[PREFETCH] Limpando Prefetch...")
    
    for item in prefetch_path.iterdir():
        try:
            if item.is_file() and item.suffix.lower() == ".pf":
                item.unlink()
        except Exception as e:
            print(f"Erro ao remover {item}: {e}")



def limpar_lixeira():
    print("\n[LIXEIRA] Esvaziando a lixeira...")
    try:
        os.system("powershell -Command Clear-RecycleBin -Force -ErrorAction SilentlyContinue")
    except Exception:
        pass
    return 0, 0

# =========================
# FUNÇÃO PRINCIPAL COM BARRA DE CARREGAMENTO DE PROGRESSO
# =========================
def limpeza_completa():
    etapas = [
        limpar_temp,
        limpar_cache,
        limpar_logs,
        limpar_prefetch,
        limpar_lixeira
    ]

    total_arquivos = 0
    total_espaco = 0

    print("\nIniciando limpeza completa...\n")

    for etapa in tqdm(etapas, desc="Progresso", ncols=100):
        arquivos, espaco = etapa()
        total_arquivos += arquivos
        total_espaco += espaco

    print("\n=========================")
    print("✔ Limpeza finalizada")
    print(f"🗂 Arquivos removidos: {total_arquivos}")
    print(f"💾 Espaço liberado: {total_espaco / (1024**2):.2f} MB")
    print("=========================")

# =========================
# EXECUÇÃO
# =========================
if __name__ == "__main__":
    limpeza_completa()