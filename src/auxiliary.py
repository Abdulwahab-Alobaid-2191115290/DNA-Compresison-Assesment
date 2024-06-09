# auxiliary functions
import os

# algorithms sends their data to this function to generate output in a suitable format (.csv)
def output(method, filepath, content_size, information_density, compression_ratio):
    filename, extension = filepath.split('\\')[-1].rsplit('.', 1)
    output_path = f'./src/output/{method}_{filename}.csv'
    if not os.path.exists(output_path):
        file = open(output_path, 'w')
        file.write(f'method,filename,extension,content_size,information_density,compression_ratio\n')
    else:
        file = open(output_path, 'a')

    file.write(f'{method},{filename},{extension},{content_size},{information_density},{compression_ratio}\n')
    file.close()

# converts two-bit binary to a nucleotide
def bin_to_base(bin):
    if bin == '00':
        return 'A'

    if bin == '01':
        return 'T'

    if bin == '10':
        return 'C'

    if bin == '11':
        return 'G'
