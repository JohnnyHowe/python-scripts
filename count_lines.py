import os

def count_non_whitespace_lines(directory):
    total_lines = 0
    total_files = 0

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.cs'):  # Adjust file extension as needed
                total_files += 1
                filepath = os.path.join(root, file)
                try: 
                    with open(filepath, 'r') as f:
                        lines = f.readlines()
                        for line in lines:
                            # if line.strip() != "":
                            total_lines += 1
                except:
                    print(f"Error reading file: {filepath}")           
    return total_lines, total_files


if __name__ == "__main__":
    directory = input("Enter the directory path: ")
    if (directory == ""):
        directory = os.getcwd()
    if (directory.startswith("/")):
        directory = os.getcwd() + "/" + directory
    lines_count, files_count = count_non_whitespace_lines(directory)
    print(f"Total number of files: {files_count}")
    print(f"Total non-whitespace lines of code: {lines_count}")
