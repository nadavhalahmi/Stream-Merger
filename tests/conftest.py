import pytest


@pytest.fixture
def basic_input() -> bytes:
    return b'!!123'


@pytest.fixture
def basic_sync() -> bytes:
    return b'!!'


@pytest.fixture
def basic_output() -> bytes:
    return b'123'
