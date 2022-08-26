from src.Translators import OffsetTranslator


def test_offset(offset_translator: OffsetTranslator, offset_input: bytes, basic_output: bytes) -> None:
    assert offset_translator.translate(
        offset_input) == [basic_output]


def test_input_is_sync(offset_translator: OffsetTranslator) -> None:
    sync = offset_translator.sync
    message = sync
    message += (sync*(offset_translator.offset -
                      1))[:offset_translator.offset-1]
    message += (2*len(sync)).to_bytes(1, 'big')
    message += sync * 2
    assert offset_translator.translate(message) == [sync * 2]


def test_random_long(offset_translator_long: OffsetTranslator, prefix_no_sync: bytes, long_rand_sync: bytes, rand_data: bytes, rand_bytes: bytes) -> None:
    assert len(rand_bytes) >= offset_translator_long.offset
    data_size = 20
    assert len(rand_data) >= data_size
    many_times = 10
    full_message = prefix_no_sync + \
        (long_rand_sync + rand_bytes[:offset_translator_long.offset - 1] +
         data_size.to_bytes(1, 'big') + rand_data[:data_size] + rand_bytes)*many_times
    window_start = 0
    output = []
    while full_message[window_start: window_start+10]:
        output = offset_translator_long.translate(
            full_message[window_start: window_start+10])
        window_start += 10
    assert output == [rand_data[:data_size]]*many_times
