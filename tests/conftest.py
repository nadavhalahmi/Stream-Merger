import pytest
from typing import List
from src import FixedTranslator


@pytest.fixture
def translator(basic_sync: bytes, basic_data_size: int) -> FixedTranslator:
    return FixedTranslator(basic_sync, basic_data_size)


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


@pytest.fixture
def inputs_2() -> List[bytes]:
    return [b'prefix!!123', b'45!!']


@pytest.fixture
def inputs_3() -> List[bytes]:
    return [b'prefix!!123', b'45!!', b'12390!']


@pytest.fixture
def inputs_4() -> List[bytes]:
    return [b'prefix!!123', b'45!!', b'12390!', b'!12345']
