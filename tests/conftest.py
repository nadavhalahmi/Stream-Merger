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


@pytest.fixture
def basic_data_size() -> int:
    return 3


@pytest.fixture
def input_with_prefix() -> bytes:
    return b'prefix!!123'
