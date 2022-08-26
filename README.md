# Stream-Merger

This project is albe to recieve bytes stream as input and print all messages found in all stream up to each input. It supports 3 different message types as described below.

There are currently 3 active branches:
- main: the main branch.
- handle-bits-resolution: reads input in bits resolution instead of bytes resolution. see #2 for more details.
- faster-complicated-translate-algorithms: a bit faster branch but more complicated.

## Clone
```
git clone https://github.com/nadavhalahmi/Stream-Merger.git
cd Stream-Merger
```

## Run
```
python3 src/main.py <message_type>
```
Where message_type is one of {fixed, offset, endseq}.

Run `python3 src/main.py -h` for further details

### Usage example
```
nadavhalahmi@Nadav-T14:~/Stream-Merger$ python3 src/main.py fixed
Please enter sync bytes:
0xf4f4
Please enter data size:
3
Please enter input:
0x112233f4f467f21a
outputs: ['0x67f21a']
Please enter input:
0x1487f4f4
outputs: ['0x67f21a']
Please enter input:
0x39a2dd7812f4
outputs: ['0x67f21a', '0x39a2dd']
Please enter input:
0xf43dace25a6c
outputs: ['0x67f21a', '0x39a2dd', '0x3dace2']
Please enter input:

nadavhalahmi@Nadav-T14:~/Stream-Merger$
```

## Tests
### Run tests using pytest:
```
pip install pytest
export PYTHONPATH=$PYTHONPATH:$PWD/src
pytest tests
```
### Run in/out tests:
```
python3 src/main.py <message_type> < inout_tests/<message_type>_in.txt > temp_out.txt
diff temp_out.txt inout_tests/<message_type>_out.txt
