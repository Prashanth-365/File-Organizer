# from home_page import HomePage
from pathlib import Path
from separate_name import extract
# home = HomePage()


files_directory = "files"
count = 0
for file_path in Path(files_directory).rglob('*.*'):
    file_name = file_path.stem  # Get the file name without extension
    file_extension = file_path.suffix  # Get the file extension
    extracted_name = extract(file_name)
    print(file_name)
    print(extracted_name)
    count += 1
print(count)

