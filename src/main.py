import re
from Translators import EndseqTranslator, FixedTranslator, OffsetTranslator, Translator
import argparse

fixed_str = 'fixed'
offset_str = 'offset'
endseq_str = 'endseq'


def message_type_descriptions():
    """
    Description for main parser. Output of `python3 main.py -h` command.
    """
    return f"""
Message type supports the following:
   {fixed_str}           - fixed message size
   {offset_str}          - offset to message size
   {endseq_str}          - ending sequence after message
"""


def read_hex(msg: str) -> bytes:
    """
    @param msg: the message to be shown to the user
    @return: this function receives input in format 0xDEADBEEF and return it as `bytes`
    """
    while True:
        s = input(msg)
        if not s:
            raise Exception("empty input")
        match = re.search(r'0x[0-9a-fA-F]+', s)
        if match and match[0] == s:
            if len(s) % 2 != 0:
                s = f'0x0{s[2:]}'
            return bytes.fromhex(s[2:])
        print("FORMAT: 0xDEADBEEF")


def read_int(msg: str) -> int:
    """
    @param msg: as in read_hex
    @return: receives positive integer input from user and return it as `int`
    """
    while True:
        s = input(msg)
        match = re.search(r'[1-9]\d*', s)
        if match and match[0] == s:
            return int(s)
        print("FORMAT: {1,2,...}")


def set_translator(message_type: str) -> Translator:
    f"""
    @param message_type: one of {fixed_str, offset_str, endseq_str}
    @return: receives sync from user and another translator based input and returns a translator
    """
    sync: bytes = read_hex("Please enter sync bytes:\n")
    if message_type == fixed_str:
        data_size: int = read_int("Please enter data size:\n")
        translator = FixedTranslator(sync, data_size)
    elif message_type == offset_str:
        offset_size: int = read_int("Please enter offset size:\n")
        translator = OffsetTranslator(sync, offset_size)
    elif message_type == endseq_str:
        endseq: bytes = read_hex("Please enter end sequence:\n")
        translator = EndseqTranslator(sync, endseq)
    else:
        raise Exception("bad message_type")
    return translator


def input_loop(translator: Translator):
    """
    reads input from user until EOF
    @param translator: translator to be used for translate user input
    """
    while True:
        try:
            input_bytes: bytes = read_hex(
                "Please enter input:\n")
        except Exception as _:  # reached EOF
            break
        outputs = translator.translate(input_bytes)
        outputs = ['0x' + o.hex() for o in outputs]
        print("outputs:", outputs)


def main():
    """
    reads sync bytes from the user, and then selects translator based on command line argument.
    translates input until EOF.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter, epilog=message_type_descriptions())
    parser.add_argument('message_type', type=str, choices=[
        fixed_str, offset_str, endseq_str], help='Arg choice.  See the choices options below')
    args = parser.parse_args()
    message_type = args.message_type

    translator: Translator = set_translator(message_type)
    input_loop(translator)


if __name__ == '__main__':
    main()
