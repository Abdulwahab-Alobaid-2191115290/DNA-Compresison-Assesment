import subprocess
from os import listdir

# collect algorithms and input files
algorithms = [f for f in listdir("./src/algorithms") if f.endswith('.py')]
input_files = [f for f in listdir("./src/input")]
# txt_input_files = [f for f in listdir("./src/input") if f.endswith('.txt')]   # used to isolate files by extension

# generate the scripts
scripts = []
for alg in algorithms:
    alg_path = f"./src/algorithms/{alg}"

    # making the <algorithm> <input> pair
    for file in input_files:
        file_path = f"./src/input/{file}"
        scripts.append(f'py {alg_path} {file_path}')

# running the scripts
for s in scripts:
    print(f"Executing: {s}")
    p = subprocess.Popen(s)
    p.wait()

# finished executing
print(f"\nFinished executing {len(algorithms)} algorithm(s) on {len(input_files)} input file(s)")
print(f"Total scripts: {len(scripts)}")
