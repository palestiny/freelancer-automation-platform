import pytest
from datetime import datetime
from app.domain.business_operations import OperationalCycle, OperationalCycleStatus, WorkItem, WorkItemStatus

def test_cycle_lifecycle():
    c=OperationalCycle('c','b',datetime(2026,1,1),datetime(2026,1,2)); c.start(); c.complete(); assert c.status == OperationalCycleStatus.COMPLETED

def test_cycle_requires_valid_period():
    with pytest.raises(ValueError): OperationalCycle('c','b',datetime(2026,1,2),datetime(2026,1,1))

def test_work_item_lifecycle():
    w=WorkItem('w','b','c','Run campaign'); w.start(); w.complete(); assert w.status == WorkItemStatus.COMPLETED

def test_failed_work_item():
    w=WorkItem('w','b','c','Run campaign'); w.start(); w.fail(); assert w.status == WorkItemStatus.FAILED

def test_work_item_cancellation():
    w=WorkItem('w','b','c','Review feedback'); w.cancel(); assert w.status == WorkItemStatus.CANCELLED
