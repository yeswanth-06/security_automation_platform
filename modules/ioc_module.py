# modules/ioc_module.py
import requests
import json
import os
from rich.console import Console
from rich.table import Table

console = Console()

def get_config_path(filename):
    """Get absolute path to config files"""
    module_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(module_dir)
    config_dir = os.path.join(project_root, 'config')
    return os.path.join(config_dir, filename)

def check_ioc(ip=None, hash_value=None, domain=None):
    """Check IOC against threat intelligence APIs"""
    
    # Load API keys from config
    try:
        api_keys_path = get_config_path('api_keys.json')
        with open(api_keys_path, 'r') as f:
            api_keys = json.load(f)
    except FileNotFoundError:
        console.print("[red]Error: config/api_keys.json not found[/red]")
        console.print("[yellow]Please create the config file with your API keys[/yellow]")
        return
    except json.JSONDecodeError:
        console.print("[red]Error: Invalid JSON in config/api_keys.json[/red]")
        return
    
    # ... rest of your existing ioc_module.py code ...
    # Determine which IOC type we have
    if ip:
        check_ip(ip, api_keys)
    elif hash_value:
        check_hash(hash_value, api_keys)
    elif domain:
        check_domain(domain, api_keys)
    else:
        console.print("[red]Error: No IOC provided[/red]")

def check_ip(ip, api_keys):
    """Check an IP against VirusTotal and AbuseIPDB"""
    table = Table(title=f"Threat Intelligence for IP: {ip}")
    table.add_column("Service")
    table.add_column("Malicious")
    table.add_column("Suspicious")
    table.add_column("Undetected")
    table.add_column("Confidence")
    
    # VirusTotal API call
    if 'virustotal' in api_keys and api_keys['virustotal'] != 'your_actual_virustotal_api_key_here':
        try:
            url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
            headers = {"x-apikey": api_keys['virustotal']}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                stats = data['data']['attributes']['last_analysis_stats']
                table.add_row(
                    "VirusTotal",
                    str(stats['malicious']),
                    str(stats['suspicious']),
                    str(stats['undetected']),
                    "N/A"
                )
            else:
                table.add_row("VirusTotal", "API Error", f"Status: {response.status_code}", "N/A", "N/A")
        except Exception as e:
            table.add_row("VirusTotal", "Error", str(e), "N/A", "N/A")
    else:
        table.add_row("VirusTotal", "Not configured", "N/A", "N/A", "N/A")
    
    # AbuseIPDB API call
    if 'abuseipdb' in api_keys and api_keys['abuseipdb'] != 'your_actual_abuseipdb_api_key_here':
        try:
            url = 'https://api.abuseipdb.com/api/v2/check'
            headers = {
                'Key': api_keys['abuseipdb'],
                'Accept': 'application/json'
            }
            params = {
                'ipAddress': ip,
                'maxAgeInDays': 90
            }
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                abuse_confidence = data['data']['abuseConfidenceScore']
                total_reports = data['data']['totalReports']
                table.add_row(
                    "AbuseIPDB",
                    str(total_reports),
                    "N/A",
                    "N/A",
                    f"{abuse_confidence}%"
                )
            else:
                table.add_row("AbuseIPDB", "API Error", f"Status: {response.status_code}", "N/A", "N/A")
        except Exception as e:
            table.add_row("AbuseIPDB", "Error", str(e), "N/A", "N/A")
    else:
        table.add_row("AbuseIPDB", "Not configured", "N/A", "N/A", "N/A")
    
    console.print(table)

def check_hash(hash_value, api_keys):
    """Check a file hash (placeholder function)"""
    console.print(f"[yellow]Hash checking for {hash_value} not yet implemented[/yellow]")

def check_domain(domain, api_keys):
    """Check a domain (placeholder function)"""
    console.print(f"[yellow]Domain checking for {domain} not yet implemented[/yellow]")