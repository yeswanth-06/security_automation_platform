# Security Automation Platform - PowerShell Wrapper
# Usage: sap [command] [options]

param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Arguments
)

# Get the directory where this script is located
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Build the command to execute
$command = @("$scriptDir/sap.py") + $Arguments

# Execute the Python script
python $command