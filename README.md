# security_automation_platform

# Security Automation Platform (SAP)

🛡️ A unified CLI tool for security automation tasks including IOC checking, Sigma rule auditing, and compliance evidence gathering.

It's a Python-based CLI platform that consolidates three key functions into one interface:

First, it performs threat intelligence lookup. You give it a suspicious IP, hash, or domain, and it queries services like VirusTotal and AbuseIPDB, presenting a unified risk score. This is great for quick triage during an incident.

Second, it validates and audits Sigma rules. Before a detection rule gets deployed to a SIEM, it checks for syntax errors, ensures it's tagged to the MITRE ATT&CK framework, and scores its overall quality. This improves the reliability of our detections.

And third, it automates compliance evidence collection. For controls like those in PCI DSS or ISO 27001, it can SSH into servers, run commands, check configurations, and automatically generate timestamped evidence files, which is a huge time-saver for audits.

The value is that it streamlines workflows, reduces context switching, and enforces consistency, all through a single tool that's easy to integrate into automated pipelines.


## Features

- **🔍 IOC Analysis**: Check IPs, hashes, and domains against threat intelligence APIs (VirusTotal, AbuseIPDB)
- **📋 Rule Auditing**: Validate and analyze Sigma rules for quality and effectiveness
- **📊 Compliance Automation**: Gather evidence for security compliance controls
- **🎨 Beautiful Output**: Rich formatted console output with colors and tables
- **⚡ Easy to Use**: Multiple installation and execution options

## Installation

### Prerequisites
- Python 3.8 or higher
- Git (for cloning the repository)

### Method 1: PIP Installation (Recommended)

# Install directly from GitHub
pip install git+https://github.com/yourusername/security_automation_platform.git

# Verify installation
sap --help


### Method 2: Clone and Install

# Clone the repository
git clone https://github.com/yourusername/security_automation_platform.git
cd security_automation_platform

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode (optional)
pip install -e .

## Quick Start

### Using the installed command (after pip install):

sap --help
sap version
sap ioc --ip 8.8.8.8

### Using Wrappers (no installation needed):

#### Windows Batch:


sap.bat --help
sap.bat ioc --ip 8.8.8.8
sap.bat audit-rule --file test_rule.yml
sap.bat gather-evidence --control TEST-1


#### PowerShell:

.\sap.ps1 --help
.\sap.ps1 ioc --ip 8.8.8.8
.\sap.ps1 audit-rule --file test_rule.yml
.\sap.ps1 gather-evidence --control TEST-1


#### Direct Python:

python sap.py --help
python sap.py ioc --ip 8.8.8.8
python sap.py audit-rule --file test_rule.yml
python sap.py gather-evidence --control TEST-1


## Configuration

### API Keys Setup
1. Copy the example configuration:

cp config/api_keys.json.example config/api_keys.json


2. Edit config/api_keys.json with your API keys:

{
    "virustotal": "your_actual_virustotal_api_key_here",
    "abuseipdb": "your_actual_abuseipdb_api_key_here"
}


3. Get free API keys:
   - [VirusTotal](https://www.virustotal.com/)
   - [AbuseIPDB](https://www.abuseipdb.com/)

### Compliance Controls
Edit config/controls.json to add your own compliance checks:

{
    "TEST-1": {
        "name": "Test Command - List Files",
        "type": "local_command",
        "command": "dir",
        "expected_pattern": "sap.py"
    }
}

## Usage Examples

### IOC Checking

# Check an IP address
sap ioc --ip 8.8.8.8

# Check a file hash
sap ioc --hash <md5_or_sha256_hash>

# Check a domain
sap ioc --domain example.com


### Sigma Rule Auditing

# Audit a Sigma rule file
sap audit-rule --file path/to/your_rule.yml

# Verbose mode for detailed analysis
sap audit-rule --file path/to/your_rule.yml --verbose


### Compliance Evidence Gathering

# Gather evidence for a control
sap gather-evidence --control TEST-1

# Specify custom output directory
sap gather-evidence --control TEST-1 --output-dir my_evidence


## Command Reference


Usage: sap [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  audit-rule       Audit and validate Sigma rules for quality, best...
  gather-evidence  Gather evidence for compliance controls through...
  ioc              Check Indicators of Compromise (IOCs) against...
  version          Show the current version of SAP.


## Project Structure


security_automation_platform/
├── config/                 # Configuration files
│   ├── api_keys.json      # API keys (create from .example)
│   └── controls.json      # Compliance control definitions
├── modules/               # Core functionality modules
│   ├── ioc_module.py      # IOC checking functionality
│   ├── rule_module.py     # Sigma rule auditing
│   └── compliance_module.py # Evidence gathering
├── evidence/              # Generated evidence files (auto-created)
├── sap.py                 # Main CLI entry point
├── setup.py               # Package installation
├── requirements.txt       # Python dependencies
├── sap.bat               # Windows batch wrapper
├── sap.ps1               # PowerShell wrapper
└── README.md             # This file


## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Make sure to install requirements:
   pip install -r requirements.txt
   
2. **API Errors**: Verify your API keys in config/api_keys.json

3. **JSON Errors**: Check your configuration files for valid JSON syntax

### Getting Help

If you encounter issues:
1. Check that all dependencies are installed
2. Verify your API keys are correct
3. Ensure you're using Python 3.8+

## Contributing

We welcome contributions! Please feel free to submit pull requests or open issues for bugs and feature requests.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Click](https://click.palletsprojects.com/) for CLI interface
- Uses [Rich](https://github.com/Textualize/rich) for beautiful console output
- Integrates with [VirusTotal](https://www.virustotal.com/) and [AbuseIPDB](https://www.abuseipdb.com/) APIs


Users can choose the method that works best for them, from simple batch file usage to proper pip installation! 🚀
