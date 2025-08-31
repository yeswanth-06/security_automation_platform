#!/usr/bin/env python3
# sap.py
import click
import os
import sys
import warnings
from cryptography.utils import CryptographyDeprecationWarning

# Suppress the specific deprecation warnings
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

# Add the current directory to Python path to find modules
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Now import the modules
from modules.ioc_module import check_ioc
from modules.rule_module import audit_rule as audit_rule_func
from modules.compliance_module import gather_evidence as gather_evidence_func

@click.group()
def cli():
    """
    🛡️  Security Automation Platform (SAP)
    
    A unified CLI tool for security tasks including:
    • IOC checking against threat intelligence services
    • Sigma rule auditing and validation  
    • Compliance evidence gathering and automation
    """
    pass

@cli.command()
@click.option('--ip', help='Check an IP address against threat intelligence services')
@click.option('--hash', help='Check a file hash (MD5, SHA1, SHA256)')
@click.option('--domain', help='Check a domain name')
def ioc(ip, hash, domain):
    """Check Indicators of Compromise (IOCs) against multiple threat intelligence APIs."""
    if not any([ip, hash, domain]):
        click.echo("❌ Error: Please provide at least one IOC (--ip, --hash, or --domain)")
        click.echo("   Example: sap ioc --ip 8.8.8.8")
        return
    
    click.echo("🔍 Querying threat intelligence services...")
    check_ioc(ip, hash, domain)

@cli.command()
@click.option('--file', required=True, help='Path to the Sigma rule file (.yml) to audit')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed analysis')
def audit_rule(file, verbose):
    """Audit and validate Sigma rules for quality, best practices, and effectiveness."""
    try:
        click.echo(f"📋 Auditing rule: {file}")
        audit_rule_func(file, verbose)
    except FileNotFoundError:
        click.echo(f"❌ Error: Rule file not found: {file}")
    except Exception as e:
        click.echo(f"❌ Error auditing rule: {e}")

@cli.command()
@click.option('--control', required=True, help='Compliance control ID (e.g., TEST-1, PCI-3.4)')
@click.option('--output-dir', default='evidence', help='Directory to save evidence files')
def gather_evidence(control, output_dir):
    """Gather evidence for compliance controls through automated checks."""
    click.echo(f"📊 Gathering evidence for control: {control}")
    gather_evidence_func(control, output_dir)

@cli.command()
def version():
    """Show the current version of SAP."""
    click.echo("🛡️  Security Automation Platform v1.0.0")

if __name__ == '__main__':
    cli()