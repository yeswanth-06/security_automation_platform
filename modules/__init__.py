# modules/__init__.py
# Import specific functions to make them available at the package level
from .ioc_module import check_ioc
from .rule_module import audit_rule
from .compliance_module import gather_evidence

# Define what gets imported with "from modules import *"
__all__ = ['check_ioc', 'audit_rule', 'gather_evidence']