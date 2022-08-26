from random import randint
import pytest
from typing import List
from src.Translators import FixedTranslator, OffsetTranslator, EndseqTranslator


@pytest.fixture
def fixed_translator(basic_sync: bytes, basic_output: bytes) -> FixedTranslator:
    return FixedTranslator(basic_sync, len(basic_output))


@pytest.fixture
def basic_sync() -> bytes:
    return b'!!'


@pytest.fixture
def basic_output() -> bytes:
    return b'123'


@pytest.fixture
def inputs(basic_sync: bytes, basic_output: bytes) -> List[bytes]:
    return [b'prefix' + basic_sync + basic_output, b'45' + basic_sync, basic_output + b'90' + basic_sync[:1],
            basic_sync[1:] + basic_output + b'45']


@pytest.fixture
def offset_translator(basic_sync: bytes, offset_size: int) -> OffsetTranslator:
    return OffsetTranslator(basic_sync, offset_size)


@pytest.fixture
def offset_translator_long(long_rand_sync: bytes, offset_size: int) -> OffsetTranslator:
    return OffsetTranslator(long_rand_sync, offset_size)


@pytest.fixture
def offset_input(basic_sync: bytes, basic_output: bytes) -> bytes:
    return basic_sync + b'@\x03' + basic_output


@pytest.fixture
def offset_size() -> int:
    return 2


@pytest.fixture
def endseq_translator(basic_sync: bytes, basic_endseq: bytes) -> EndseqTranslator:
    return EndseqTranslator(basic_sync, basic_endseq)


@pytest.fixture
def endseq_translator_sync_is_endseq(basic_sync: bytes) -> EndseqTranslator:
    return EndseqTranslator(basic_sync, basic_sync)


@pytest.fixture
def endseq_input(basic_sync: bytes, basic_endseq: bytes, basic_output: bytes) -> bytes:
    return basic_sync + basic_output + basic_endseq


@pytest.fixture
def basic_endseq() -> bytes:
    return b'@@@'


@pytest.fixture
def long_sync_size() -> int:
    return 40


@pytest.fixture
def long_data_size(long_sync_size: int) -> int:
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


@pytest.fixture
def fixed_translator_long_sync(long_rand_sync: bytes, basic_output: bytes) -> FixedTranslator:
    return FixedTranslator(long_rand_sync, len(basic_output))


@pytest.fixture
def fixed_translator_bits_example() -> FixedTranslator:
    return FixedTranslator(b'\xFF', 2)
