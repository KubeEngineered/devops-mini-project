import ipaddress

# Set of single malicious IPs (fast lookup)
BLOCKED_IPS = {
    "192.168.1.100",
    "203.0.113.45",
}

# List of malicious IP subnets/ranges
BLOCKED_NETWORKS = [
    ipaddress.ip_network("198.51.100.0/24"),
    ipaddress.ip_network("45.33.0.0/16"),
]

def is_ip_blocked(client_ip_str: str) -> bool:
    """
    Checks if a given IP address string is blocked.
    """
    try:
        ip = ipaddress.ip_address(client_ip_str)
    except ValueError:
        # Invalid IP format; block or handle as bad request
        return True

    # Check direct IP lookup
    if str(ip) in BLOCKED_IPS:
        return True

    # Check subnets
    for network in BLOCKED_NETWORKS:
        if ip in network:
            return True

    return False

# --- Example Usage ---
requests = ["192.168.1.100", "198.51.100.22", "8.8.8.8"]

for req_ip in requests:
    if is_ip_blocked(req_ip):
        print(f"[REJECT 403] Traffic blocked from {req_ip}")
    else:
        print(f"[ACCEPT 200] Traffic allowed from {req_ip}")
