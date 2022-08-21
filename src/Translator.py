from typing import List


class Translator:
    def __init__(self, sync: bytes, data_size: int):
        self.sync: bytes = sync
        self.data_size: int = data_size
        self.input_so_far: bytes = b''

    def translate(self, input_bytes: bytes) -> List[bytes]:
        self.input_so_far += input_bytes
        splited_so_far: List[bytes] = self.input_so_far.split(self.sync)[1:]
        splited_so_far = list(
            filter(lambda x: x, map(
                lambda s: s[:self.data_size], splited_so_far)))
        return splited_so_far
