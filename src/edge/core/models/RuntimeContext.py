"""
A RuntimeContext is meant to store the ReportModels returned from each command in a Routine.
"""
from collections import defaultdict

class RuntimeContext:
    def __init__(self):
        self.reports = defaultdict(list)
        self.terminated_by = None
        self.terminated_at_chain_id = None