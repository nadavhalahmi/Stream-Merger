from src import *
from typing import List


def test_basic(translator: Translator, basic_input: bytes, basic_sync: bytes, basic_output: bytes, basic_data_size: int) -> None:
    assert translator.translate(
        basic_input) == [basic_output]


def test_ignore_first_bytes(translator: Translator, input_with_prefix: bytes, basic_sync: bytes, basic_output: bytes, basic_data_size: int) -> None:
    assert translator.translate(input_with_prefix) == [basic_output]


def test_2_inputs_1_output(translator: Translator, inputs_2: List[bytes], basic_sync: bytes, basic_output: bytes, basic_data_size: int) -> None:
    assert translator.translate(inputs_2[0]) == [basic_output]
    assert translator.translate(inputs_2[1]) == [basic_output]


def test_3_inputs_2_outputs(translator: Translator, inputs_3: List[bytes], basic_sync: bytes, basic_output: bytes, basic_data_size: int) -> None:
    assert translator.translate(inputs_3[0], ) == [basic_output]
    assert translator.translate(inputs_3[1]) == [basic_output]
    assert translator.translate(inputs_3[2]) == [basic_output, basic_output]
