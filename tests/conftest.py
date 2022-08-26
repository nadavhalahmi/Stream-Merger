from random import randint
import pytest
from typing import List, Tuple
from src.Translators import FixedTranslator, OffsetTranslator, EndseqTranslator


@pytest.fixture
def basic_sync() -> bytes:
    return b'!!'


@pytest.fixture
def basic_output() -> bytes:
    return b'123'


@pytest.fixture
def long_sync_size() -> int:
    return 40


@pytest.fixture
def long_sync_range() -> Tuple[int, int]:
    return (0, 32)


@pytest.fixture
def long_data_size(long_sync_size: int) -> int:
    return long_sync_size*3


@pytest.fixture
def long_rand_sync(long_sync_size: int, long_sync_range: Tuple[int, int]) -> bytes:
    sync: bytes = b''
    for _ in range(long_sync_size):
        sync += randint(long_sync_range[0],
                        long_sync_range[1]).to_bytes(1, 'big')
    return sync


@pytest.fixture
def rand_bytes_no_sync(long_sync_size: int, long_sync_range: Tuple[int, int]) -> bytes:
    rand_bytes: bytes = b''
    for _ in range(2):
        for _ in range(long_sync_size):
            rand_bytes += randint(long_sync_range[1]+1,
                                  (long_sync_range[1]+1)*2).to_bytes(1, 'big')
    return rand_bytes


@pytest.fixture
def rand_bytes(long_data_size: int, long_sync_range: Tuple[int, int]) -> bytes:
    rand_data: bytes = b''
    for _ in range(long_data_size):
        rand_data += randint(long_sync_range[0],
                             long_sync_range[1]).to_bytes(1, 'big')
    return rand_data


@pytest.fixture
def fixed_translator(basic_sync: bytes, basic_output: bytes) -> FixedTranslator:
    return FixedTranslator(basic_sync, len(basic_output))


@pytest.fixture
def fixed_inputs(basic_sync: bytes, basic_output: bytes) -> List[bytes]:
    return [b'prefix' + basic_sync + basic_output, b'45' + basic_sync, basic_output + b'90' + basic_sync[:1],
            basic_sync[1:] + basic_output + b'45']


@pytest.fixture
def fixed_translator_long(long_rand_sync: bytes, long_data_size: int) -> FixedTranslator:
    return FixedTranslator(long_rand_sync, long_data_size)


@pytest.fixture
def fixed_translator_long_sync(long_rand_sync: bytes, basic_output: bytes) -> FixedTranslator:
    return FixedTranslator(long_rand_sync, len(basic_output))


@pytest.fixture
def offset_size() -> int:
    return 2


@pytest.fixture
def offset_input(basic_sync: bytes, basic_output: bytes) -> bytes:
    return basic_sync + b'@\x03' + basic_output


@pytest.fixture
def offset_translator(basic_sync: bytes, offset_size: int) -> OffsetTranslator:
    return OffsetTranslator(basic_sync, offset_size)


@pytest.fixture
def offset_translator_long(long_rand_sync: bytes, offset_size: int) -> OffsetTranslator:
    return OffsetTranslator(long_rand_sync, offset_size)


@pytest.fixture
def basic_endseq() -> bytes:
    return b'@@@'


@pytest.fixture
def endseq_input(basic_sync: bytes, basic_endseq: bytes, basic_output: bytes) -> bytes:
    return basic_sync + basic_output + basic_endseq


@pytest.fixture
def endseq_translator(basic_sync: bytes, basic_endseq: bytes) -> EndseqTranslator:
    return EndseqTranslator(basic_sync, basic_endseq)


@pytest.fixture
def endseq_translator_sync_is_endseq(basic_sync: bytes) -> EndseqTranslator:
    return EndseqTranslator(basic_sync, basic_sync)
