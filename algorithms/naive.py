import sys

if len(sys.argv[1:]) != 1:
    print(f'Error: invalid args')
    print(f'Usage: py {sys.argv[0]} <input file>')
    sys.exit(1)

file = open(sys.argv[1], 'r')
src = file.read()
file.close()

def bin_to_base(bin):
    if bin == '00':
        return 'A'

    if bin == '01':
        return 'T'

    if bin == '10':
        return 'C'

    if bin == '11':
        return 'G'


src_binary = ''
for char in src:
    block = '0'+bin(ord(char))[2:]
    src_binary += block

if len(src_binary) % 2 != 0:
    src_binary = '0' + src_binary
print(src_binary)
encoding = ''
src_binary_tmp = src_binary
print(len(src_binary_tmp))
while len(src_binary_tmp) != 0:
    bin = src_binary_tmp[:2]
    encoding += bin_to_base(bin)
    src_binary_tmp = src_binary_tmp[2:]


print(encoding)

bits = len(src_binary)
bases = len(encoding)
information_density = bits / bases
compressed_size = bases*2
compression_ratio = bits / compressed_size

print(f'information density {bits/bases}, compression ratio {compression_ratio}')

file = open('./output/naive.csv', 'w')
file.write(f'method,content_size,extension,information_density,compression_ratio\n')
file.write(f'naive,{len(src)},txt,{information_density},{compression_ratio}')
file.close()
