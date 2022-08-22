import pytest
from typing import List
from src import FixedTranslator, OffsetTranslator
from src.Translators import EndseqTranslator


@pytest.fixture
def fixed_translator(basic_sync: bytes, basic_data_size: int) -> FixedTranslator:
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


@pytest.fixture
def offset_translator(basic_sync: bytes, offset_size: int) -> OffsetTranslator:
    return OffsetTranslator(basic_sync, offset_size)


@pytest.fixture
def offset_input() -> bytes:
    return b'!!@\x03123'


@pytest.fixture
def offset_size() -> int:
    return 2


@pytest.fixture
def endseq_translator(basic_sync: bytes, endseq: bytes) -> EndseqTranslator:
    return EndseqTranslator(basic_sync, endseq)


@pytest.fixture
def endseq_input() -> bytes:
    return b'!!123@@@'


@pytest.fixture
def endseq() -> bytes:
    return b'@@@'
