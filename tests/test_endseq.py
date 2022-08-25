from src import *
from src.Translators import EndseqTranslator


def test_endseq(endseq_translator: EndseqTranslator, endseq_input: bytes, basic_output: bytes) -> None:
    assert endseq_translator.translate(
        endseq_input) == [basic_output]


def test_basic_2_inputs_2_outpus(endseq_translator: EndseqTranslator, endseq_input: bytes, basic_output: bytes) -> None:
    assert endseq_translator.translate(endseq_input) == [basic_output]
    assert endseq_translator.translate(endseq_input) == [basic_output]*2
