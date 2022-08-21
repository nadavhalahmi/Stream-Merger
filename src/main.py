from Translator import Translator
from typing import List, Optional
import argparse

fixed = 'fixed'
offset = 'offset'
endseq = 'endseq'


def message_type_descriptions():
    return f"""
Message type supports the following:
   {fixed}           - fixed message size
   {offset}          - offset to message size
   {endseq}          - ending sequence after message
"""


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter, epilog=message_type_descriptions())
    parser.add_argument('message_type', type=str, choices=[
                        fixed, offset, endseq], help='Arg choice.  See the choices options below')
    args = parser.parse_args()
    message_type = args.message_type
    translator: Optional[Translator] = None
    sync: bytes = input("Please enter sync bytes:\n").encode()
    if message_type == fixed:
        data_size: int = int(input("Please enter data size:\n"))
        translator = Translator(sync, data_size)
    elif message_type == offset:
        return 0
    elif message_type == endseq:
        return 0
    else:
        return 0
    outputs: List[bytes] = []
    while True:
        input_bytes: bytes = input("Please enter input:\n").encode()
        if not input_bytes:
            break
        outputs = translator.translate(input_bytes)
        print(outputs)


if __name__ == '__main__':
    main()
