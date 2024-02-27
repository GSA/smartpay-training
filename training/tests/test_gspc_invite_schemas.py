import pytest
from datetime import datetime
from training.schemas.gspc_invite import GspcInvite

@pytest.fixture
def single_valid_input():
    return "test1@example.com"

@pytest.fixture
def valid_input():
    return "test1@example.com, test2@example.com"

@pytest.fixture
def invalid_input():
    return "invalid_email, @example.com, test3"

@pytest.fixture
def mixed_input():
    return "test1@example.com, test2@example.com, invalid_email, @example.com, test3"

@pytest.fixture
def gspc_invite():
    return GspcInvite(email_addresses="", certification_expiration_date=datetime.now())

def test_parse_single_valid_email(single_valid_input, gspc_invite):
    gspc_invite.email_addresses = single_valid_input
    gspc_invite.parse()
    assert gspc_invite.valid_emails == ['test1@example.com']

def test_parse_valid_emails(valid_input, gspc_invite):
    gspc_invite.email_addresses = valid_input
    gspc_invite.parse()
    assert gspc_invite.valid_emails == ['test1@example.com', 'test2@example.com']

def test_parse_invalid_emails(invalid_input, gspc_invite):
    gspc_invite.email_addresses = invalid_input
    gspc_invite.parse()
    assert gspc_invite.invalid_emails == ['invalid_email', '@example.com', 'test3']

def test_parse_mixed_emails(mixed_input, gspc_invite):
    gspc_invite.email_addresses = mixed_input
    gspc_invite.parse()
    assert gspc_invite.valid_emails == ['test1@example.com', 'test2@example.com']
    assert gspc_invite.invalid_emails == ['invalid_email', '@example.com', 'test3']

def test_parse_empty_input(gspc_invite):
    gspc_invite.parse()
    assert gspc_invite.valid_emails == []
    assert gspc_invite.invalid_emails == []

def test_parse_no_input(gspc_invite):
    gspc_invite.email_addresses = None
    gspc_invite.parse()
    assert gspc_invite.valid_emails == []
    assert gspc_invite.invalid_emails == []