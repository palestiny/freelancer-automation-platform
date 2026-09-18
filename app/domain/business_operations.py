from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class OperationalCycleStatus(str, Enum):
    PLANNED = 'planned'
    RUNNING = 'running'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

class WorkItemStatus(str, Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'

@dataclass
class OperationalCycle:
    id: str
    business_id: str
    period_start: datetime
    period_end: datetime
    status: OperationalCycleStatus = OperationalCycleStatus.PLANNED
    def __post_init__(self):
        if not self.id or not self.business_id: raise ValueError('id and business_id are required')
        if self.period_end <= self.period_start: raise ValueError('period_end must be after period_start')
    def start(self):
        if self.status != OperationalCycleStatus.PLANNED: raise ValueError('cycle can only start when planned')
        self.status = OperationalCycleStatus.RUNNING
    def complete(self):
        if self.status != OperationalCycleStatus.RUNNING: raise ValueError('cycle can only complete when running')
        self.status = OperationalCycleStatus.COMPLETED

@dataclass
class WorkItem:
    id: str
    business_id: str
    cycle_id: str
    title: str
    status: WorkItemStatus = WorkItemStatus.PENDING
    def __post_init__(self):
        if not self.id or not self.business_id or not self.cycle_id or not self.title: raise ValueError('work item identity and title are required')
    def start(self):
        if self.status != WorkItemStatus.PENDING: raise ValueError('work item can only start when pending')
        self.status = WorkItemStatus.IN_PROGRESS
    def complete(self):
        if self.status != WorkItemStatus.IN_PROGRESS: raise ValueError('work item can only complete when in progress')
        self.status = WorkItemStatus.COMPLETED
    def fail(self):
        if self.status != WorkItemStatus.IN_PROGRESS: raise ValueError('work item can only fail when in progress')
        self.status = WorkItemStatus.FAILED
    def cancel(self):
        if self.status in (WorkItemStatus.COMPLETED, WorkItemStatus.CANCELLED): raise ValueError('completed or cancelled work cannot be cancelled')
        self.status = WorkItemStatus.CANCELLED
