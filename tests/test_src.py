from src import *
from typing import List


def test_basic(basic_input: bytes, basic_sync: bytes, basic_output: bytes, basic_data_size: int) -> None:
    assert translate(basic_input, basic_sync, basic_data_size) == basic_output


def test_ignore_first_bytes(input_with_prefix: bytes, basic_sync: bytes, basic_output: bytes, basic_data_size: int) -> None:
    assert translate(input_with_prefix, basic_sync,
                     basic_data_size) == basic_output


def test_2_inputs_1_output(inputs: List[bytes], basic_sync: bytes, basic_output: bytes, basic_data_size: int) -> None:
    assert translate(inputs[0], basic_sync,
                     basic_data_size) == basic_output
    assert translate(inputs[1], basic_sync,
                     basic_data_size) == b''
