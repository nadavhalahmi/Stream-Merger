from src import *
from src.Translators import EndseqTranslator


def test_endseq(endseq_translator: EndseqTranslator, endseq_input: bytes, basic_output: bytes) -> None:
    assert endseq_translator.translate(
        endseq_input) == [basic_output]


def test_basic_2_inputs_2_outpus(endseq_translator: EndseqTranslator, endseq_input: bytes, basic_output: bytes) -> None:
    assert endseq_translator.translate(endseq_input) == [basic_output]
    assert endseq_translator.translate(endseq_input) == [basic_output]*2


def test_sync_is_endseq(endseq_translator_sync_is_endseq: EndseqTranslator, basic_sync: bytes) -> None:
    simple_data = b'simple data'
    msg = basic_sync + simple_data + basic_sync
    assert endseq_translator_sync_is_endseq.translate(msg) == [simple_data]


def test_random_long(endseq_translator: EndseqTranslator, rand_data: bytes, rand_bytes: bytes) -> None:
    many_times = 10
    sync = endseq_translator.sync
    endseq = endseq_translator.endseq
    full_msg = rand_data + (sync + rand_data + endseq)*many_times
    window_start = 0
    output = []
    while full_msg[window_start: window_start+10]:
        output = endseq_translator.translate(
            full_msg[window_start: window_start+10])
        window_start += 10
    assert output == [rand_data]*many_times
