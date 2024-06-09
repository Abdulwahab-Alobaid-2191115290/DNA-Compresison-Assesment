import sys
import os

# so we can import aux
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import auxiliary as aux

# command line args: each algorithm takes input file in command line
if len(sys.argv[1:]) != 1:
    print(f'Error: invalid args')
    print(f'Usage: py {sys.argv[0]} <input file>')
    sys.exit(1)

# reading file contents
filepath = sys.argv[1]
file = open(filepath, 'r')
src = file.read()
file.close()


# getting the binary representation of the file
src_binary = ''
for char in src:
    block = '0'+bin(ord(char))[2:]
    src_binary += block

# appending 0s if length is odd
if len(src_binary) % 2 != 0:
    src_binary = '0' + src_binary

# basic encoding implementation: split into two-bit strings -> convert to base -> append bases
encoding = ''
src_binary_tmp = src_binary
while len(src_binary_tmp) != 0:
    bin = src_binary_tmp[:2]
    encoding += aux.bin_to_base(bin)
    src_binary_tmp = src_binary_tmp[2:]

# calculate evaluation metrics
bits = len(src_binary)
bases = len(encoding)
information_density = bits / bases
compressed_size = bases*2
compression_ratio = bits / compressed_size

# print results
print(encoding)
print(f'information density {bits/bases}, compression ratio {compression_ratio}')

# generate output
aux.output(
        method='basic',
        filepath=filepath,
        content_size=len(src),
        information_density=information_density,
        compression_ratio=compression_ratio
)
