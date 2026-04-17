# def get_windows_info():
#    return "Windows (detecção simplificada)"

# Tentativa de requerimento de informação do Windows de forma alternativa

import platform 
import psutil
import wmi
# Traz estas informações, mas com a Biblioteca "psutil", temos informações detalhadas como RAM, Tecnologia de uso (DDR), e Frequência. CPU e Disco que estão sendo usados.
def get_windows_info():
    info = {}
    info['sistema'] = platform.system()
    info['versao'] = platform.version()
    info['release'] = platform.release()
    info['arquitetura'] = platform.architecture()
    info['maquina'] = platform.node()
    info['processador'] = platform.processor()
# Detectando a versão do Windows sendo utilizada pelo usuário
    if info['sistema'] == 'Windows':
        build = int(platform.version().split('.')[-1])
    info['build'] = build
    if build >= 22000:
        info['edicao_windows'] = 'Windows 11'
    else:
        info['edicao_windows'] = 'Windows 10 ou anterior'
# Informações da CPU
    info['cpu_nome'] = platform.processor()
    if platform.system() == "Windows":
        try:
            import _wmi
            c = wmi.WMI()
            for cpu in c.Win32_Processor():
                nome = cpu.Name.strip()
                nucleos = cpu.NumberOfCores
                threads = cpu.NumberOfLogicalProcessors
                freq = cpu.MaxClockSpeed
                info['cpu_nome'] = f'{nome}, {freq} MHz, {nucleos} Núcleo(s), {threads} Processador(es) Lógico(s)'
        except Exception:
            pass

    # Trazendo Informações da RAM - Usando A unidade de medida internacional (Por mil, ao invés de binário 1024)
    memoria = psutil.virtual_memory()
    info['ram_total_gb'] = round(memoria.total / (1000**3), 2)
    info['ram_disponivel_gb'] = round(memoria.available / (1000**3), 2)

    # Trazendo informações do Disco usado no PC
    disco = psutil.disk_usage('C:\\')
    info['disco_total_gb'] = round(disco.total / (1000**3), 2)
    info['disco_usado_gb'] = round(disco.used / (1000**3), 2)

    return info
print(get_windows_info())
