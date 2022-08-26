from src import *
from typing import List


def test_basic(fixed_translator: FixedTranslator, basic_output: bytes) -> None:
    assert fixed_translator.translate(
        fixed_translator.sync + basic_output) == [basic_output]


def test_ignore_first_bytes(fixed_translator: FixedTranslator, basic_output: bytes) -> None:
    assert fixed_translator.translate(
        b'prefix' + fixed_translator.sync + basic_output) == [basic_output]


def test_2_inputs_1_output(fixed_translator: FixedTranslator, inputs: List[bytes], basic_output: bytes) -> None:
    assert fixed_translator.translate(inputs[0]) == [basic_output]
    assert fixed_translator.translate(inputs[1]) == [basic_output]


def test_3_inputs_2_outputs(fixed_translator: FixedTranslator, inputs: List[bytes], basic_output: bytes) -> None:
    assert fixed_translator.translate(inputs[0]) == [basic_output]
    assert fixed_translator.translate(inputs[1]) == [basic_output]
    assert fixed_translator.translate(inputs[2]) == [
        basic_output, basic_output]


def test_4_inputs_3_outputs(fixed_translator: FixedTranslator, inputs: List[bytes], basic_output: bytes) -> None:
    assert fixed_translator.translate(inputs[0]) == [basic_output]
    assert fixed_translator.translate(inputs[1]) == [basic_output]
    assert fixed_translator.translate(inputs[2]) == [
        basic_output, basic_output]
    assert fixed_translator.translate(inputs[3]) == [
        basic_output, basic_output, basic_output]


def test_input_is_sync(fixed_translator: FixedTranslator) -> None:
    basic_input_size = len(fixed_translator.sync) + \
        fixed_translator.data_size
    input_full_of_sync = (fixed_translator.sync *
                          basic_input_size)[:basic_input_size]
    assert fixed_translator.translate(input_full_of_sync) == [
        input_full_of_sync[len(fixed_translator.sync):]]


def test_random_long(fixed_translator_long: FixedTranslator, prefix_no_sync: bytes, long_rand_sync: bytes, rand_data: bytes, rand_bytes: bytes) -> None:
    many_times = 10
    full_message = prefix_no_sync + \
        (long_rand_sync+rand_data+rand_bytes)*many_times
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


def test_bits(fixed_translator_bits_example: FixedTranslator) -> None:
    """
    see https://github.com/nadavhalahmi/Stream-Merger/issues/2
    """
    assert fixed_translator_bits_example.translate(
        b'\x3F\xC0\x40\x40') == [b'\x01\x01']
