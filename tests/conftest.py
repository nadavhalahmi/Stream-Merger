from random import randint
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


@pytest.fixture
def long_sync_size() -> int:
    return 40


@pytest.fixture
def long_data_size(long_sync_size) -> int:
    return long_sync_size*3


@pytest.fixture
def long_rand_sync(long_sync_size: int) -> bytes:
    """bytes [0-!(33))(exclusive), size=long_sync_size"""
    sync: bytes = b''
    for _ in range(long_sync_size):
        sync += randint(0, 32).to_bytes(1, 'big')
    return sync


@pytest.fixture
def prefix_no_sync(long_sync_size: int) -> bytes:
    prefix: bytes = b''
    for _ in range(2):
        for _ in range(long_sync_size-1):
            prefix += randint(0, 32).to_bytes(1, 'big')
        prefix += (33).to_bytes(1, 'big')
    return prefix


@pytest.fixture
def rand_data(long_data_size: int) -> bytes:
    rand_data: bytes = b''
    for _ in range(long_data_size):
        rand_data += randint(0, 33).to_bytes(1, 'big')
    return rand_data


@pytest.fixture
def rand_bytes(prefix_no_sync: bytes) -> bytes:
    return prefix_no_sync


@pytest.fixture
def fixed_translator_long(long_rand_sync: bytes, long_data_size: int) -> FixedTranslator:
    return FixedTranslator(long_rand_sync, long_data_size)
