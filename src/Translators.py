from typing import List


class Translator:
    """
    Used as basic Translator.
    @param sync: sync bytes for messages. Represents start of message.
    """
    def __init__(self, sync: bytes):
        self.sync: bytes = sync
        self.sync_size = len(sync)
        self.input_so_far: bytes = b''
        self.outputs_so_far: List[bytes] = []

    def translate(self, input_bytes: bytes) -> List[bytes]:
        """
        @param input_bytes: bytes to translate
        @return list of all translated inputs to far
        """
        pass


class FixedTranslator(Translator):
    """
    Example:
    FixedTranslator(0xAA,2): 0x99AA11223344AA5566 -> [0x1122, 0x5566]
    @param sync: as in Translator
    @param data_size: size of data after sync. data after data_size is ignored until next sync
    """
    def __init__(self, sync: bytes, data_size: int):
        super().__init__(sync)
        self.data_size: int = data_size
        self.message_size = self.sync_size + data_size

    def translate(self, input_bytes: bytes) -> List[bytes]:
        """
        As in example
        @param input_bytes: as in Translator
        @return: as in Translator
        """
        self.input_so_far += input_bytes
        if self.message_size > len(self.input_so_far):
            return self.outputs_so_far  # input_so_far can't hold a full message
        window = (0, self.sync_size)
        last_output = -1
        while window[1] + self.data_size - 1 < len(self.input_so_far):
            if self.input_so_far[window[0]:window[1]] == self.sync:
                self.outputs_so_far.append(
                    self.input_so_far[window[1]:window[1] + self.data_size])
                last_output = window[0] + self.message_size - 1
                window = (window[0] + self.message_size,
                          window[1] + self.message_size)
            else:
                window = (window[0] + 1, window[1] + 1)
        self.input_so_far = self.input_so_far[last_output+1:]
        return self.outputs_so_far


class OffsetTranslator(Translator):
    """
    Example:
    OffsetTranslator(AA,2): 0x99AAFF02112233AAEE013344 -> [0x1122, 0x33]
    @param sync: as in Translator
    @param offset_size: offset to size of message
    """
    def __init__(self, sync: bytes, offset_size: int):
        super().__init__(sync)
        self.offset_size: int = offset_size

    def translate(self, input_bytes: bytes) -> List[bytes]:
        """
        As in example
        @param input_bytes: as in Translator
        @return: as in Translator
        """
        self.input_so_far += input_bytes
        if self.sync_size + self.offset_size > len(self.input_so_far):
            # input_so_far can't even hold sync+offset, surly can't hold data too
            return self.outputs_so_far
        window = (0, self.sync_size)
        last_output = -1
        while window[1] + self.offset_size - 1 < len(self.input_so_far):
            if self.input_so_far[window[0]:window[1]] == self.sync:
                data_size = int(
                    self.input_so_far[window[1] + self.offset_size - 1])
                msg_size = self.sync_size + self.offset_size+data_size
                if window[1] + self.offset_size+data_size > len(self.input_so_far):
                    self.input_so_far = self.input_so_far[last_output+1:]
                    return self.outputs_so_far
                self.outputs_so_far.append(
                    self.input_so_far[window[1] + self.offset_size:window[1] + self.offset_size + data_size])
                last_output = window[0] + msg_size - 1
                window = (window[0] + msg_size,
                          window[1] + msg_size)
            else:
                window = (window[0] + 1, window[1] + 1)
        self.input_so_far = self.input_so_far[last_output+1:]
        return self.outputs_so_far


class EndseqTranslator(Translator):
    """
    Example:
    EndseqTranslator(AA,BB): 0x99AA1122BB33AA445566BB -> [0x1122, 0x445566]
    @param sync: as in Translator
    @param endseq: a sequence of bytes representing end of message.
    """
    def __init__(self, sync: bytes, endseq: bytes):
        super().__init__(sync)
        self.endseq: bytes = endseq
        self.endseq_size: int = len(self.endseq)

    def translate(self, input_bytes: bytes) -> List[bytes]:
        """
        As in example
        @param input_bytes: as in Translator
        @return: as in Translator
        """
        self.input_so_far += input_bytes
        if self.sync_size + self.endseq_size > len(self.input_so_far):
            # input_so_far can't even hold sync+endseq, surly can't hold data too
            return self.outputs_so_far
        sync_window = (0, self.sync_size)
        last_output = -1
        while sync_window[1] <= len(self.input_so_far):
            if self.input_so_far[sync_window[0]:sync_window[1]] == self.sync:
                endseq_window = (
                    sync_window[1], sync_window[1]+self.endseq_size)
                while endseq_window[1] <= len(self.input_so_far):
                    if self.input_so_far[endseq_window[0]:endseq_window[1]] == self.endseq:
                        data = self.input_so_far[sync_window[1]:endseq_window[0]]
                        self.outputs_so_far.append(data)
                        last_output = endseq_window[1]-1
                        break
                    else:
                        endseq_window = (
                            endseq_window[0] + 1, endseq_window[1] + 1)
                sync_window = (endseq_window[1],
                               endseq_window[1] + self.sync_size)
            else:
                sync_window = (sync_window[0] + 1, sync_window[1] + 1)
        self.input_so_far = self.input_so_far[last_output+1:]
        return self.outputs_so_far
