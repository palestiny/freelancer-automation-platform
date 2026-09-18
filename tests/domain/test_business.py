import pytest
from app.domain.business import Business, BusinessStatus

def test_business_lifecycle():
    b=Business('b1','Example','model-1'); b.start_validation(); b.start_operations(); b.pause(); b.resume(); b.close(); assert b.status == BusinessStatus.CLOSED

def test_business_requires_identity():
    with pytest.raises(ValueError): Business('','','model')
    with pytest.raises(ValueError): Business('b','name','')

def test_invalid_transition():
    with pytest.raises(ValueError): Business('b','name','model').start_operations()
