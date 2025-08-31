# modules/compliance_module.py
import json
import paramiko
import subprocess
import os
from datetime import datetime
from rich.console import Console

console = Console()

def gather_evidence(control_id, output_dir='evidence'):
    """Gather evidence for a specific compliance control"""
    # Load control definitions
    try:
        with open('config/controls.json', 'r') as f:
            controls = json.load(f)
    except FileNotFoundError:
        console.print(f"[red]Error: config/controls.json not found[/red]")
        return
    except json.JSONDecodeError as e:
        console.print(f"[red]Error: Invalid JSON in config/controls.json: {e}[/red]")
        return
    
    if control_id not in controls:
        console.print(f"[red]Error: Control {control_id} not found in controls.json[/red]")
        return
    
    control = controls[control_id]
    console.print(f"[green]Gathering evidence for {control_id}: {control['name']}[/green]")
    
    # Execute command based on control type
    result_output = ""
    if control['type'] == 'ssh_command':
        result_output = execute_ssh_command(
            control['host'],
            control['username'],
            control.get('password'),
            control.get('key_file'),
            control['command']
        )
        
    elif control['type'] == 'local_command':
        try:
            result = subprocess.run(control['command'], shell=True, capture_output=True, text=True)
            result_output = f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}\n\nRETURN CODE: {result.returncode}"
        except Exception as e:
            result_output = f"Error executing command: {str(e)}"
    else:
        result_output = f"Unknown control type: {control['type']}"
    
    # Save evidence
    save_evidence(control_id, control['command'], result_output, control.get('expected_pattern'), output_dir)

def execute_ssh_command(host, username, password, key_file, command):
    """Execute a command on a remote host via SSH"""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        if key_file:
            key = paramiko.RSAKey.from_private_key_file(key_file)
            client.connect(hostname=host, username=username, pkey=key)
        else:
            client.connect(hostname=host, username=username, password=password)
        
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        
        return f"STDOUT:\n{output}\n\nSTDERR:\n{error}"
    
    except Exception as e:
        return f"SSH Error: {str(e)}"
    
    finally:
        client.close()

def save_evidence(control_id, command, output, expected_pattern=None, output_dir='evidence'):
    """Save evidence to file with timestamp"""
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/{control_id}_{timestamp}.txt"
    
    status = "PASS"
    if expected_pattern and expected_pattern not in output:
        status = "FAIL"
    
    try:
        with open(filename, 'w') as f:
            f.write(f"Control ID: {control_id}\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            f.write(f"Command: {command}\n")
            f.write(f"Status: {status}\n")
            f.write("\n" + "="*50 + "\n")
            f.write("OUTPUT:\n")
            f.write("="*50 + "\n")
            f.write(output)
        
        console.print(f"[green]Evidence saved to: {filename}[/green]")
        console.print(f"[green]Status: {status}[/green]")
        
    except Exception as e:
        console.print(f"[red]Error saving evidence: {e}[/red]")