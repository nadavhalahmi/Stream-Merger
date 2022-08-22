from typing import List
import re


class FixedTranslator:
    def __init__(self, sync: bytes, data_size: int):
        self.sync: bytes = sync
        self.data_size: int = data_size
        self.sync_size = len(sync)
        self.message_size = self.sync_size + data_size
        self.input_so_far: bytes = b''

    def translate(self, input_bytes: bytes) -> List[bytes]:
        self.input_so_far += input_bytes
        if self.message_size > len(self.input_so_far):
            return []  # input_so_far can't hold a full message
        window = (0, self.sync_size)
        res: List[bytes] = []
        while window[1] + self.data_size - 1 < len(self.input_so_far):
            if self.input_so_far[window[0]:window[1]] == self.sync:
                res.append(
                    self.input_so_far[window[1]:window[1] + self.data_size])
                window = (window[0] + self.message_size,
                          window[1] + self.message_size)
            else:
                window = (window[0] + 1, window[1] + 1)
        return res


class OffsetTranslator:
    def __init__(self, sync: bytes, offset_size: int):
        self.sync: bytes = sync
        self.offset_size: int = offset_size
        self.input_so_far: bytes = b''

    def translate(self, input_bytes: bytes) -> List[bytes]:
        self.input_so_far += input_bytes
        splited_so_far: List[bytes] = self.input_so_far.split(self.sync)[1:]
        splited_so_far = list(
            filter(lambda x: x, map(
                lambda s: s[self.offset_size:self.offset_size + s[self.offset_size-1]], splited_so_far)))  # TODO: fix
        return splited_so_far


class EndseqTranslator:
    def __init__(self, sync: bytes, endseq: bytes):
        self.sync: bytes = sync
        self.endseq: bytes = endseq
        self.input_so_far: bytes = b''
        self.pattern: bytes = self.sync+b'(.*)'+self.endseq

    def translate(self, input_bytes: bytes) -> List[bytes]:
        self.input_so_far += input_bytes
        splited_so_far: List[bytes] = re.findall(
            self.pattern, self.input_so_far)
        return splited_so_far
