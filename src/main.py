def translate(input_bytes: bytes, sync: bytes) -> bytes:
    return input_bytes[2:]


def main():
    sync: bytes = input("Please enter sync bytes:\n")
    input_bytes: bytes = input("Please enter input:\n")
    output: bytes = translate(input_bytes, sync)
    print(output)


if __name__ == '__main__':
    main()
