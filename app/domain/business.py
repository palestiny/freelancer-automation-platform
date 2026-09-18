from dataclasses import dataclass
from enum import Enum

class BusinessStatus(str, Enum):
    PLANNING = 'planning'
    VALIDATING = 'validating'
    OPERATING = 'operating'
    PAUSED = 'paused'
    CLOSED = 'closed'

@dataclass
class Business:
    id: str
    name: str
    business_model_id: str
    status: BusinessStatus = BusinessStatus.PLANNING

    def __post_init__(self):
        if not self.id or not self.name or not self.business_model_id:
            raise ValueError('id, name, and business_model_id are required')

    def start_validation(self):
        if self.status != BusinessStatus.PLANNING: raise ValueError('business can only start validation from planning')
        self.status = BusinessStatus.VALIDATING

    def start_operations(self):
        if self.status != BusinessStatus.VALIDATING: raise ValueError('business can only start operations from validating')
        self.status = BusinessStatus.OPERATING

    def pause(self):
        if self.status != BusinessStatus.OPERATING: raise ValueError('only operating businesses can be paused')
        self.status = BusinessStatus.PAUSED

    def resume(self):
        if self.status != BusinessStatus.PAUSED: raise ValueError('only paused businesses can resume')
        self.status = BusinessStatus.OPERATING

    def close(self):
        if self.status == BusinessStatus.CLOSED: raise ValueError('business is already closed')
        self.status = BusinessStatus.CLOSED
