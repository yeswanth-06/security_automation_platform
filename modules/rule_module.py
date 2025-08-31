# modules/rule_module.py
import yaml
from rich.console import Console
from rich.table import Table

console = Console()

def audit_rule(file_path, verbose=False):
    """Audit a Sigma rule for quality and effectiveness"""
    try:
        with open(file_path, 'r') as f:
            rule = yaml.safe_load(f)
        
        if not rule:
            console.print("[red]Error: Rule file is empty or invalid[/red]")
            return
        
        table = Table(title=f"Rule Audit for: {file_path}")
        table.add_column("Check", style="cyan")
        table.add_column("Status", style="bold")
        table.add_column("Details")
        
        # Check for title
        if 'title' not in rule:
            table.add_row("Title", "[red]FAIL[/red]", "Rule has no title")
        else:
            title = str(rule['title'])
            table.add_row("Title", "[green]PASS[/green]", f"Title: {title}")
        
        # Check for MITRE ATT&CK tags
        if 'tags' not in rule:
            table.add_row("MITRE Tags", "[red]FAIL[/red]", "No tags section")
        else:
            tags = rule['tags']
            if isinstance(tags, list):
                mitre_tags = [str(tag) for tag in tags if 'attack.' in str(tag)]
            else:
                mitre_tags = [str(tags)] if 'attack.' in str(tags) else []
                
            if len(mitre_tags) == 0:
                table.add_row("MITRE Tags", "[yellow]WARN[/yellow]", "No MITRE ATT&CK tags found")
            else:
                table.add_row("MITRE Tags", "[green]PASS[/green]", f"Found {len(mitre_tags)} MITRE tags: {', '.join(mitre_tags)}")
        
        # Check for log source
        if 'logsource' not in rule:
            table.add_row("Log Source", "[red]FAIL[/red]", "No logsource defined")
        else:
            logsource = rule['logsource']
            if logsource and isinstance(logsource, dict):
                details = f"Category: {logsource.get('category', 'N/A')}, Product: {logsource.get('product', 'N/A')}"
                table.add_row("Log Source", "[green]PASS[/green]", details)
            else:
                table.add_row("Log Source", "[yellow]WARN[/yellow]", "Logsource defined but empty or invalid")
        
        # Check for detection condition
        if 'detection' not in rule:
            table.add_row("Detection", "[red]FAIL[/red]", "No detection condition")
        else:
            detection = rule['detection']
            if detection and isinstance(detection, dict) and len(detection) > 0:
                table.add_row("Detection", "[green]PASS[/green]", "Detection condition exists")
            else:
                table.add_row("Detection", "[yellow]WARN[/yellow]", "Detection defined but empty")
        
        # Check for status field
        if 'status' not in rule:
            table.add_row("Status", "[yellow]WARN[/yellow]", "No status field defined")
        else:
            status = str(rule['status'])
            table.add_row("Status", "[green]PASS[/green]", f"Status: {status}")
        
        console.print(table)
        
    except yaml.YAMLError as e:
        console.print(f"[red]Error parsing YAML file: {e}[/red]")
    except FileNotFoundError:
        console.print(f"[red]Error: Rule file not found: {file_path}[/red]")
    except Exception as e:
        console.print(f"[red]Error auditing rule: {e}[/red]")
        if verbose:
            import traceback
            console.print(f"[yellow]Detailed traceback:[/yellow]")
            console.print(traceback.format_exc())