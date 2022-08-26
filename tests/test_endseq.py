from src.Translators import EndseqTranslator


def test_endseq(endseq_translator: EndseqTranslator, endseq_input: bytes, basic_output: bytes) -> None:
    assert endseq_translator.translate(
        endseq_input) == [basic_output]


def test_basic_2_inputs_2_outputs(endseq_translator: EndseqTranslator, endseq_input: bytes, basic_output: bytes) -> None:
    assert endseq_translator.translate(endseq_input) == [basic_output]
    assert endseq_translator.translate(endseq_input) == [basic_output]*2


def test_sync_is_endseq(endseq_translator_sync_is_endseq: EndseqTranslator, basic_sync: bytes) -> None:
    simple_data = b'simple data'
    message = basic_sync + simple_data + basic_sync
    assert endseq_translator_sync_is_endseq.translate(message) == [simple_data]


def test_random_long(endseq_translator: EndseqTranslator, rand_bytes_no_sync: bytes) -> None:
    many_times = 10
    sync = endseq_translator.sync
    endseq = endseq_translator.endseq
    full_message = rand_bytes_no_sync + \
        (sync + rand_bytes_no_sync + endseq)*many_times
    window_start = 0
    output = []
    while full_message[window_start: window_start+10]:
        output = endseq_translator.translate(
            full_message[window_start: window_start+10])
        window_start += 10
    assert output == [rand_bytes_no_sync]*many_times
