from system_utils import executar_comando

def flush_dns():
    return executar_comando(
        "ipconfig /flushdns",
        "systemd-resolve --flush-caches",
        "dscacheutil -flushcache"
    )

def renew_ip():
    return executar_comando(
        "ipconfig /renew",
        "dhclient",
        None
    )

def ping():
    return executar_comando(
        "ping google.com -n 4",
        "ping -c 4 google.com",
        "ping -c 4 google.com"
    )
