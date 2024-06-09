import time
import sys
import os

# so we can import aux
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import auxiliary as aux

def get_key_from_val(val, d):
    for key in d:
        if d[key] == val:
            return key

# nodes definition that will be used to implement m.v. huffman tree
class Node:
    def __init__(self, symbol=None, pfreq=0, left=None, right=None, distance=0, path=''):
        self.symbol = symbol
        self.pfreq = pfreq
        self.distance = distance

        self.edge = None
        self.left = left
        self.right = right
        self.path = path

    # prints the tree nicely, used for debugging, but becomes crowded on large input
    def visual_print(self, indent=0):
        if self.right:
            self.right.visual_print(indent + 4)

        print(' ' * indent + f'{self.symbol}{self.pfreq}-D{self.distance}')

        if self.left:
            self.left.visual_print(indent + 4)

    # prints nodes and their frequencies
    def print(self, node=None):

        if not node:
            node = self

        if node.left:
            self.print(node.left)

        print(f'{node.symbol}{node.pfreq}', end=' ')

        if node.right:
            self.print(node.right)


class Tree:

    def __init__(self, src, symbols):
        self.cookbook = {}
        self.c_cookbook = {}
        self.global_cookbook = {}
        self.path_sym = {}

        # get probabilities of each symbol
        freq = symbols
        prob = {}
        for sym in freq:
            prob[sym] = round(freq[sym]/len(src), 2)


        # generate initial tree e.g. [A3, G2, ...]
        self.tree = []
        for sym in prob:
            self.tree.append(Node(symbol=sym, pfreq=prob[sym]))

    # prints each node
    def print(self):
        # print nodes
        for node in self.tree:
            node.print()
        print()

    # readable version of the tree, but becomes crowded for large input
    def visual_print(self):
        # print nodes
        for node in self.tree:
            node.visual_print()
        print()

    # returns the first and second minimum nodes by pfreq, this is used for merging
    def get_minimums(self):
        # first minimum
        f_min = self.tree[0]
        for node in self.tree:
            if node.pfreq < f_min.pfreq:
                f_min = node

        # second minimum
        s_min = self.tree[0]
        for node in self.tree:
            if node.pfreq < s_min.pfreq and (node.symbol != f_min.symbol):
                s_min = node

        # if tree contains only two children then they are the only nodes to be merged
        if len(self.tree) == 2:
            f_min, s_min = self.tree[0], self.tree[1]

        return f_min, s_min

    # merges the tree once: to complete the tree this function is called multiple times
    def merge_once(self):
        # get first and second minimums
        f_min, s_min = self.get_minimums()

        # merge by creating a node having the sum of both nodes freq
        print(f'merging {f_min.symbol}{f_min.pfreq} >< {s_min.symbol}{s_min.pfreq}')
        merged = Node(symbol=f_min.symbol + ';' + s_min.symbol, pfreq=f_min.pfreq + s_min.pfreq, left=f_min, right=s_min)

        # update the tree
        self.tree = [node for node in self.tree if node.symbol != f_min.symbol and node.symbol != s_min.symbol]
        self.tree.append(merged)

    # sets the distance to the root from each node: should only be called when huffman tree is completed
    # when calling the function, the tree contains only one element i.e. the root
    def set_distance(self, node=None, distance=0):
        # break
        if not node and distance != 0:
            return

        # if calling first time, set the node to be the root
        if distance == 0:
            node = self.tree[0]

        # distance increases whenever we go deeper in the tree, hence add 1 for each level
        if node.right:
            self.set_distance(node.right, distance + 1)

        # set current distance
        node.distance = distance

        # set left distance
        if node.left:
            self.set_distance(node.left, distance + 1)

    # sets the encoding or rather "path" of each node, according to GC and RunLength constraints
    def set_path(self, node=None, path=''):
        if not node and path != '':
            return

        if path == '':
            node = self.tree[0]

        if node.left:
            base = 'A' if node.distance % 2 == 0 else 'G'
            self.set_path(node.left, path + base)

        node.path = path
        if not node.right and not node.left:
            print(f'{node.symbol}: {node.path}')
            self.path_sym[path] = node.symbol
            self.cookbook[path] = node.symbol

        if node.right:
            base = 'T' if node.distance % 2 == 0 else 'C'
            self.set_path(node.right, path + base)


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


# calculate symbols and their frequencies
src_binary = ''
sliced = []
symbols = {}
for char in src:
    block = '0'+bin(ord(char))[2:]  # gets ascii of the char
    src_binary += block             # generates the binary block by block
    sliced.append(block)            # add blocks in an array
    symbols[block] = symbols.get(block, 0) + 1  # stores symbols and their frequencies

# print(f'\nsymbols: {symbols}')

# generate tree
tree = Tree(src, symbols)

# print tree
print('\nInitial nodes:')
tree.print()
print()

# constructing m.v. huffman tree by merging nodes repeatedly
while len(tree.tree) > 1:
    tree.merge_once()
print()

print('\nM.V. Huffman Tree: \n')
tree.set_distance()     # sets distance from root to each node
tree.set_path()         # generates the encoding (which is the path in the tree) for each char
tree.visual_print()     # prints the resulting tree

# generate complimentary cookbook
for sym in tree.cookbook:
    strand = tree.cookbook[sym]
    c_strand = ''

    for base in sym:
        if base == 'A':
            c_strand += 'G'
        elif base == 'G':
            c_strand += 'A'
        elif base == 'C':
            c_strand += 'T'
        elif base == 'T':
            c_strand += 'C'

    tree.c_cookbook[c_strand] = strand

# global cook book is used to determine how to switch between original and complementary cook books
tree.global_cookbook = {True: tree.cookbook, False: tree.c_cookbook}
print(f'\ntree global cookbook: {tree.global_cookbook}')

# generate encoding
encoding = ''
current_cookbook = True     # flags the current cook book, either original or complimentary
for block in sliced:
    # get the encoding of this symbol (block)
    coding = get_key_from_val(block, tree.global_cookbook[current_cookbook])
    if len(coding) % 2 != 0:
        # flip cookbook
        current_cookbook = not current_cookbook
    encoding += coding

print(f'\ntree.path_sym: \n{tree.path_sym}')
print(f'\nsliced: \n{sliced}')
print(f'\nencoding:\n{encoding} \n')

# decoding algorithm is applied to ensure we can get the original string back
decoding = ''
dnadecoding = ''
current_cookbook = True
encoding_tmp = encoding
print('Decoding: ')
while len(encoding_tmp) != 0:

    idx = 0
    olgo = encoding_tmp[idx]

    # should look in the current cookbook
    block = tree.global_cookbook[current_cookbook].get(olgo, None)

    # while olgo is not a path(encoding)
    while block is None:
        next_base = encoding_tmp[idx + 1: idx + 2]
        idx += 1

        olgo += next_base
        block = tree.global_cookbook[current_cookbook].get(olgo, None)
        time.sleep(0.3)

    if len(olgo) % 2 != 0:
        current_cookbook = not current_cookbook

    decoding += block
    dnadecoding += olgo
    encoding_tmp = encoding_tmp[idx + 1:]
    print(olgo, end= '')
print()

# verification
if encoding == dnadecoding:
    print('\nDecoded successfully')

    # calculate evaluation metrics
    bits = len(sliced)*8
    bases = len(dnadecoding)
    information_density = bits/bases

    compressed_size = len(dnadecoding)*2

    compression_ratio = bits/compressed_size

    print(f'information density {bits/bases}, compression ratio {compression_ratio}')

    aux.output(
        method='mv_huffman',
        filepath=filepath,
        content_size=len(src),
        information_density=information_density,
        compression_ratio=compression_ratio
    )
else:
    print('\nOops, decoding error:')
    print(f'original: {encoding}\ndecoded: {dnadecoding}')






