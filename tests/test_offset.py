from src import *
from src.Translators import OffsetTranslator


def test_offset(offset_translator: OffsetTranslator, offset_input: bytes, basic_sync: bytes, basic_output: bytes, basic_data_size: int) -> None:
    assert offset_translator.translate(
        offset_input) == [basic_output]
