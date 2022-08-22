from Translators import EndseqTranslator, FixedTranslator, OffsetTranslator, Translator
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


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter, epilog=message_type_descriptions())
    parser.add_argument('message_type', type=str, choices=[
                        fixed_str, offset_str, endseq_str], help='Arg choice.  See the choices options below')
    args = parser.parse_args()
    message_type = args.message_type
    sync: bytes = input("Please enter sync bytes:\n").encode()
    if message_type == fixed_str:
        data_size: int = int(input("Please enter data size:\n"))
        translator = FixedTranslator(sync, data_size)
    elif message_type == offset_str:
        offset_size: int = int(input("Please enter offset size:\n"))
        translator = OffsetTranslator(sync, offset_size)
    elif message_type == endseq_str:
        endseq: bytes = input("Please enter end sequence:\n").encode()
        translator = EndseqTranslator(sync, endseq)
    else:
        return 0
    while True:
        input_bytes: bytes = input("Please enter input:\n").encode()
        if not input_bytes:
            break
        outputs = translator.translate(input_bytes)
        print(outputs)


if __name__ == '__main__':
    main()
