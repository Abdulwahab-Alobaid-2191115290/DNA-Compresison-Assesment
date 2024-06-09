# auxiliary functions
import os

# algorithms sends their data to this function to generate output in a suitable format (.csv)
def output(method, filepath, content_size, information_density, compression_ratio):

    # thanks to windows, if running script from terminal the path uses \ regardless what
    # you exactly type in the terminal. if running script using 'subprocess' library the path uses
    # the other slash i.e. /
    # so to fix this we check first what slash type is passed to the function
    # PS: this also means if the input filename includes slashes; it will pose a problem
    if '/' in filepath:
        filename, extension = filepath.split('/')[-1].rsplit('.', 1)
    elif '\\' in filepath:
        filename, extension = filepath.split('\\')[-1].rsplit('.', 1)
    else:
        print('ERROR: slash character in the path is not \\ or /')
        exit(-1)

    # if file exists, append new entry, else create the file and add the headers
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
