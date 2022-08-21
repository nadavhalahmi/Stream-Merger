from src import *
from typing import List


def test_basic(translator: Translator, basic_input: bytes, basic_sync: bytes, basic_output: bytes, basic_data_size: int) -> None:
    assert translator.translate(
        basic_input, basic_sync, basic_data_size) == basic_output


def test_ignore_first_bytes(translator: Translator, input_with_prefix: bytes, basic_sync: bytes, basic_output: bytes, basic_data_size: int) -> None:
    assert translator.translate(input_with_prefix, basic_sync,
                                basic_data_size) == basic_output


def test_2_inputs_1_output(translator: Translator, inputs: List[bytes], basic_sync: bytes, basic_output: bytes, basic_data_size: int) -> None:
    assert translator.translate(inputs[0], basic_sync,
                                basic_data_size) == basic_output
    assert translator.translate(inputs[1], basic_sync,
                                basic_data_size) == b''
