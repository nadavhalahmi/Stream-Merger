import re
from src.Translators import EndseqTranslator, FixedTranslator, OffsetTranslator
import argparse


fixed_str = 'fixed'
offset_str = 'offset'
endseq_str = 'endseq'


def message_type_descriptions():
    return f"""
Message type supports the following:
   {fixed_str}           - fixed message size
   {offset_str}          - offset to message size
   {endseq_str}          - ending sequence after message
"""


def read_hex(msg: str) -> bytes:
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
    while True:
        s = input(msg)
        match = re.search(r'[1-9]\d*', s)
        if match and match[0] == s:
            return int(s)
        print("FORMAT: {1,2,...}")


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter, epilog=message_type_descriptions())
    parser.add_argument('message_type', type=str, choices=[
                        fixed_str, offset_str, endseq_str], help='Arg choice.  See the choices options below')
    args = parser.parse_args()
    message_type = args.message_type
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
        return 0
    while True:
        try:
            input_bytes: bytes = read_hex(
                "Please enter input:\n")
        except Exception as _:
            break
        outputs = translator.translate(input_bytes)
        outputs = ['0x' + o.hex() for o in outputs]
        print("outputs:", outputs)


if __name__ == '__main__':
    main()
