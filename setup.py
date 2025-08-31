# setup.py
from setuptools import setup

setup(
    name="security-automation-platform",
    version="1.0.0",
    description="A unified CLI tool for security automation tasks",
    py_modules=['sap'],  # This tells setuptools about sap.py
    install_requires=[
        "click==8.1.7",
        "requests==2.31.0",
        "PyYAML==6.0.1",
        "paramiko==3.4.0",
        "rich==13.7.0",
    ],
    entry_points={
        "console_scripts": [
            "sap=sap:cli",  # This points to the cli function in sap.py
        ],
    },
    python_requires=">=3.8",
)