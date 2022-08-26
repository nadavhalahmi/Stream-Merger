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
        curr_sync = self.input_so_far.find(self.sync)
        # while found sync and have enough room for a message
        while curr_sync != -1 and curr_sync + self.message_size - 1 < len(self.input_so_far):
            data_range = (curr_sync + self.sync_size,
                          curr_sync + self.sync_size + self.data_size)
            self.outputs_so_far.append(
                self.input_so_far[data_range[0]:data_range[1]])  # add data after sync
            self.input_so_far = self.input_so_far[data_range[1]:]
            curr_sync = self.input_so_far.find(self.sync)
        return self.outputs_so_far


class OffsetTranslator(Translator):
    """
    Example:
    OffsetTranslator(AA,2): 0x99AAFF02112233AAEE013344 -> [0x1122, 0x33]
    @param sync: as in Translator
    @param offset: offset to size of message
    """

    def __init__(self, sync: bytes, offset: int):
        super().__init__(sync)
        self.offset: int = offset

    def translate(self, input_bytes: bytes) -> List[bytes]:
        """
        As in example
        @param input_bytes: as in Translator
        @return: as in Translator
        """
        self.input_so_far += input_bytes
        curr_sync = self.input_so_far.find(self.sync)
        while curr_sync != -1 and curr_sync + self.sync_size + self.offset - 1 < len(self.input_so_far):
            data_size = int(
                self.input_so_far[curr_sync + self.sync_size + self.offset - 1])
            data_range = (curr_sync + self.sync_size + self.offset,
                          curr_sync + self.sync_size + self.offset + data_size)
            # no room for a message
            if data_range[1] > len(self.input_so_far):
                return self.outputs_so_far
            # add data to outputs_so_far
            self.outputs_so_far.append(
                self.input_so_far[data_range[0]:data_range[1]])
            self.input_so_far = self.input_so_far[data_range[1]:]
            curr_sync = self.input_so_far.find(self.sync)
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
        curr_sync = self.input_so_far.find(self.sync)
        while curr_sync != -1 and curr_sync + self.sync_size + self.endseq_size - 1 < len(self.input_so_far):
            # found sync, now find endseq
            curr_endseq = self.input_so_far[curr_sync +
                                            self.sync_size:].find(self.endseq)
            if curr_endseq != -1:  # found endseq after sync
                data_range = (curr_sync + self.sync_size,
                              curr_sync+self.sync_size+curr_endseq)
                data = self.input_so_far[data_range[0]:data_range[1]]
                self.outputs_so_far.append(data)
                self.input_so_far = self.input_so_far[data_range[1] +
                                                      self.endseq_size:]
            else:
                return self.outputs_so_far
            curr_sync = self.input_so_far.find(self.sync)
        return self.outputs_so_far
