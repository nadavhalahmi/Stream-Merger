def translate(input_bytes: bytes, sync: bytes, data_size: int) -> bytes:
    return input_bytes.split(sync)[-1]


def main():
    sync: bytes = input("Please enter sync bytes:\n")
    data_size: int = int(input("Please enter data size:\n"))
    input_bytes: bytes = input("Please enter input:\n")
    output: bytes = translate(input_bytes, sync, data_size)
    print(output)


if __name__ == '__main__':
    main()
