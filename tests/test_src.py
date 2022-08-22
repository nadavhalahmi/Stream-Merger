from src import *
from typing import List


def test_basic(fixed_translator: FixedTranslator, basic_input: bytes, basic_sync: bytes, basic_output: bytes, basic_data_size: int) -> None:
    assert fixed_translator.translate(
        basic_input) == [basic_output]


def test_ignore_first_bytes(fixed_translator: FixedTranslator, input_with_prefix: bytes, basic_sync: bytes, basic_output: bytes, basic_data_size: int) -> None:
    assert fixed_translator.translate(input_with_prefix) == [basic_output]


def test_2_inputs_1_output(fixed_translator: FixedTranslator, inputs_2: List[bytes], basic_sync: bytes, basic_output: bytes, basic_data_size: int) -> None:
    assert fixed_translator.translate(inputs_2[0]) == [basic_output]
    assert fixed_translator.translate(inputs_2[1]) == [basic_output]


def test_3_inputs_2_outputs(fixed_translator: FixedTranslator, inputs_3: List[bytes], basic_sync: bytes, basic_output: bytes, basic_data_size: int) -> None:
    assert fixed_translator.translate(inputs_3[0], ) == [basic_output]
    assert fixed_translator.translate(inputs_3[1]) == [basic_output]
    assert fixed_translator.translate(inputs_3[2]) == [
        basic_output, basic_output]


def test_4_inputs_3_outputs(fixed_translator: FixedTranslator, inputs_4: List[bytes], basic_sync: bytes, basic_output: bytes, basic_data_size: int) -> None:
    assert fixed_translator.translate(inputs_4[0], ) == [basic_output]
    assert fixed_translator.translate(inputs_4[1]) == [basic_output]
    assert fixed_translator.translate(inputs_4[2]) == [
        basic_output, basic_output]
    assert fixed_translator.translate(inputs_4[3]) == [
        basic_output, basic_output, basic_output]


def test_input_is_sync(fixed_translator: FixedTranslator, basic_sync: bytes, basic_data_size: int) -> None:
    basic_input_size = len(basic_sync) + basic_data_size
    input_full_of_sync = (basic_sync*basic_input_size)[:basic_input_size]
    assert fixed_translator.translate(input_full_of_sync) == [
        input_full_of_sync[len(basic_sync):]]


def test_random_long(fixed_translator_long: FixedTranslator, prefix_no_sync: bytes, long_rand_sync: bytes, rand_data: bytes, rand_bytes: bytes) -> None:
    many_times = 10
    full_msg = prefix_no_sync + \
        (long_rand_sync+rand_data+rand_bytes)*many_times
    window_start = 0
    output = []
    while full_msg[window_start: window_start+10]:
        output = fixed_translator_long.translate(
            full_msg[window_start: window_start+10])
        window_start += 10
    assert output == [rand_data]*many_times
