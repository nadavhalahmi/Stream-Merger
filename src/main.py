from typing import List

# from src.Translator import Translator
from Translator import Translator


def main():
    sync: bytes = input("Please enter sync bytes:\n").encode()
    data_size: int = int(input("Please enter data size:\n"))
    outputs: List[bytes] = []
    translator: Translator = Translator(sync, data_size)
    while True:
        input_bytes: bytes = input("Please enter input:\n").encode()
        if not input_bytes:
            break
        outputs = translator.translate(input_bytes)
        print(outputs)


if __name__ == '__main__':
    main()
