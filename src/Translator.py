class Translator:
    input_so_far: bytes = b''

    def translate(self, input_bytes: bytes, sync: bytes, data_size: int) -> bytes:
        self.input_so_far += input_bytes
        return input_bytes.split(sync)[-1]
