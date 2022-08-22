from src.Translators import OffsetTranslator


def test_offset(offset_translator: OffsetTranslator, offset_input: bytes, basic_output: bytes) -> None:
    assert offset_translator.translate(
        offset_input) == [basic_output]


def test_input_is_sync(offset_translator: OffsetTranslator) -> None:
    sync = offset_translator.sync
    msg = sync
    msg += (sync*(offset_translator.offset_size -
                  1))[:offset_translator.offset_size-1]
    msg += (2*len(sync)).to_bytes(1, 'big')
    msg += sync * 2
    assert offset_translator.translate(msg) == [sync * 2]
