from src import *


def test_basic(basic_input: bytes, basic_sync: bytes, basic_output: bytes, basic_data_size: int) -> None:
    assert translate(basic_input, basic_sync, basic_data_size) == basic_output


def test_ignore_first_bytes(input_with_prefix: bytes, basic_sync: bytes, basic_output: bytes, basic_data_size: int) -> None:
    assert translate(input_with_prefix, basic_sync,
                     basic_data_size) == basic_output
