from src import *
from typing import List


def test_basic(fixed_translator: FixedTranslator, basic_output: bytes) -> None:
    assert fixed_translator.translate(
        fixed_translator.sync + basic_output) == [basic_output]


def test_ignore_first_bytes(fixed_translator: FixedTranslator, basic_output: bytes) -> None:
    assert fixed_translator.translate(
        b'prefix' + fixed_translator.sync + basic_output) == [basic_output]


def test_2_inputs_1_output(fixed_translator: FixedTranslator, fixed_inputs: List[bytes], basic_output: bytes) -> None:
    assert fixed_translator.translate(fixed_inputs[0]) == [basic_output]
    assert fixed_translator.translate(fixed_inputs[1]) == [basic_output]


def test_3_inputs_2_outputs(fixed_translator: FixedTranslator, fixed_inputs: List[bytes], basic_output: bytes) -> None:
    assert fixed_translator.translate(fixed_inputs[0]) == [basic_output]
    assert fixed_translator.translate(fixed_inputs[1]) == [basic_output]
    assert fixed_translator.translate(fixed_inputs[2]) == [
        basic_output, basic_output]


def test_4_inputs_3_outputs(fixed_translator: FixedTranslator, fixed_inputs: List[bytes], basic_output: bytes) -> None:
    assert fixed_translator.translate(fixed_inputs[0]) == [basic_output]
    assert fixed_translator.translate(fixed_inputs[1]) == [basic_output]
    assert fixed_translator.translate(fixed_inputs[2]) == [
        basic_output, basic_output]
    assert fixed_translator.translate(fixed_inputs[3]) == [
        basic_output, basic_output, basic_output]


def test_input_is_sync(fixed_translator: FixedTranslator) -> None:
    basic_input_size = len(fixed_translator.sync) + \
        fixed_translator.data_size
    input_full_of_sync = (fixed_translator.sync *
                          basic_input_size)[:basic_input_size]
    assert fixed_translator.translate(input_full_of_sync) == [
        input_full_of_sync[len(fixed_translator.sync):]]


def test_random_long(fixed_translator_long: FixedTranslator, rand_bytes_no_sync: bytes, rand_bytes: bytes, long_rand_sync: bytes) -> None:
    many_times = 10
    data_size = fixed_translator_long.data_size
    rand_data = (rand_bytes*data_size)[:data_size]
    full_message = rand_bytes_no_sync + \
        (long_rand_sync + rand_data + rand_bytes)*many_times
    window_start = 0
    output = []
    while full_message[window_start: window_start+10]:
        output = fixed_translator_long.translate(
            full_message[window_start: window_start+10])
        window_start += 10
    assert output == [rand_data]*many_times


def test_long_sync(fixed_translator_long_sync: FixedTranslator, long_rand_sync: bytes, basic_output: bytes) -> None:
    message = long_rand_sync + basic_output
    assert fixed_translator_long_sync.data_size == len(basic_output)
    assert fixed_translator_long_sync.translate(message) == [basic_output]
