import sys

# command line args
if len(sys.argv[1:]) != 1:
    print(f'Error: invalid args')
    print(f'Usage: py {sys.argv[0]} <input file>')
    sys.exit(1)

# reading file contents
file = open(sys.argv[1], 'r')
src = file.read()
file.close()

# function that converts from two-bit binary to a nucleotide
def bin_to_base(bin):
    if bin == '00':
        return 'A'

    if bin == '01':
        return 'T'

    if bin == '10':
        return 'C'

    if bin == '11':
        return 'G'

# creating tree nodes
class NodeTree(object):

    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return (self.left, self.right)

    def nodes(self):
        return (self.left, self.right)

    def __str__(self):
        return '%s_%s' % (self.left, self.right)


# main function implementing huffman coding
def huffman_code_tree(node, left=True, binString=''):
    if type(node) is str:
        return {node: binString}
    (l, r) = node.children()
    d = dict()
    d.update(huffman_code_tree(l, True, binString + '0'))
    d.update(huffman_code_tree(r, False, binString + '1'))
    return d


# calculating frequency
freq = {}
for c in src:
    if c in freq:
        freq[c] += 1
    else:
        freq[c] = 1

freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
nodes = freq

while len(nodes) > 1:
    (key1, c1) = nodes[-1]
    (key2, c2) = nodes[-2]
    nodes = nodes[:-2]
    node = NodeTree(key1, key2)
    nodes.append((node, c1 + c2))

    nodes = sorted(nodes, key=lambda x: x[1], reverse=True)

huffmanCode = huffman_code_tree(nodes[0][0])

print(' Char | Huffman code ')
print('----------------------')
for (char, frequency) in freq:
    print(' %-4r |%12s' % (char, huffmanCode[char]))

src_binary = ''
for char in src:
    src_binary += huffmanCode[char]
print(src_binary)

if len(src_binary) % 2 != 0:
    src_binary = '0' + src_binary

encoding = ''
src_binary_tmp = src_binary
while len(src_binary_tmp) != 0:
    bin = src_binary_tmp[:2]
    encoding += bin_to_base(bin)
    src_binary_tmp = src_binary_tmp[2:]
print(encoding)

bits = len(src)*8
bases = len(encoding)
information_density = bits / bases
compressed_size = len(encoding)*2
compression_ratio = bits/compressed_size

print(f'information density {bits / bases}, compression ratio {compression_ratio}%')

file = open('./output/huffman.csv', 'w')
file.write(f'method,content_size,extension,information_density,compression_ratio\n')
file.write(f'huffman,{len(src)},txt,{information_density},{compression_ratio}')
file.close()
