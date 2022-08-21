from src import *


def test_basic(basic_input: bytes, basic_sync: bytes, basic_output: bytes) -> None:
    assert translate(basic_input, basic_sync) == basic_output
