import os
import requests


input_folder = "source"
output_folder = "raw"

# Check if cs2_decompile.exe exists, if not download it
if not os.path.exists("cs2_decompile.exe"):
    url = "https://github.com/trigger-segfault/catsystem-py/blob/unstable/tool/trigger/cs2_decompile.exe?raw=true"
    response = requests.get(url)
    with open("cs2_decompile.exe", "wb") as file:
        file.write(response.content)

# Get paths to each script file in current directory and subdirectories
script_files = []
for root, dirs, filenames in os.walk(f'./{input_folder}'):
    for filename in filenames:
        if filename.endswith(".cst"):
            script_files.append(os.path.join(root, filename))

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
# Convert each script file
for script_file in script_files:
    # run cs2_decompile.exe on each script file to output human readable text (-hr)
    os.system(f'cs2_decompile.exe {script_file} -o {output_folder} -md')
    # remove the human from the output file
    file_name = os.path.basename(script_file).split('.')[0]
    os.rename(f'{output_folder}/{file_name}.human.md', f'{output_folder}/{file_name}.txt')