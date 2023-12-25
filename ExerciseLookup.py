import zipfile
import os
import ast
import pandas as pd
import openpyxl

def extract_zip_file():
    # Prompt the user for the path of the ZIP file
    zip_file_path = input("Please enter the path of the ZIP file to extract: ")

    # Prompt the user for the directory where they want to save the extracted files
    save_directory = input("Please enter the directory where you want to save the extracted files: ")

    try:
        # Opening the zip file using 'with' statement
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(save_directory)
            print(f"Files extracted successfully to {save_directory}")
    except FileNotFoundError:
        print("ZIP file not found. Please check the file path.")
    except zipfile.BadZipFile:
        print("The file is not a zip file or it is corrupted.")
    except Exception as e:
        print(f"An error occurred: {e}")

def save_dataframe_to_excel():
    # Prompt the user for the Excel file path where they want to save the DataFrame
    excel_file_path = input("Please enter the path where you want to save the Excel file: ")

    try:
        # Save the DataFrame as an Excel file with the 'xlsx' engine
        df_analysis.to_excel(excel_file_path, index=False, engine='xlsx')
        print(f"DataFrame saved successfully to {excel_file_path}")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")

# Function to get all Python files from a directory, including subdirectories
def get_python_files(directory):
    python_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

# List of built-in Python functions (as of Python 3.8)
builtin_functions = [
    'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'breakpoint', 'bytearray', 'bytes',
    'callable', 'chr', 'classmethod', 'compile', 'complex', 'delattr', 'dict',
    'dir', 'divmod', 'enumerate', 'eval', 'exec', 'filter', 'float', 'format',
    'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id',
    'input', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'list', 'locals',
    'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord',
    'pow', 'print', 'property', 'range', 'repr', 'reversed', 'round', 'set',
    'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple',
    'type', 'vars', 'zip', '__import__'
]

# Methods for standard Python types
standard_methods = {
    "str": [
        "capitalize", "casefold", "center", "count", "encode", "endswith", "expandtabs",
        "find", "format", "format_map", "index", "isalnum", "isalpha", "isascii",
        "isdecimal", "isdigit", "isidentifier", "islower", "isnumeric", "isprintable",
        "isspace", "istitle", "isupper", "join", "ljust", "lower", "lstrip",
        "maketrans", "partition", "replace", "rfind", "rindex", "rjust", "rpartition",
        "rsplit", "rstrip", "split", "splitlines", "startswith", "strip", "swapcase",
        "title", "translate", "upper", "zfill"
    ],
    "list": [
        "append", "clear", "copy", "count", "extend", "index", "insert", "pop", "remove",
        "reverse", "sort"
    ],
    "dict": [
        "clear", "copy", "fromkeys", "get", "items", "keys", "pop", "popitem", "setdefault",
        "update", "values"
    ],
    "set": [
        "add", "clear", "copy", "difference", "difference_update", "discard", "intersection",
        "intersection_update", "isdisjoint", "issubset", "issuperset", "pop", "remove",
        "symmetric_difference", "symmetric_difference_update", "union", "update"
    ],
    "tuple": ["count", "index"],
    "file": [
        "close", "detach", "fileno", "flush", "isatty", "read", "readable", "readline",
        "readlines", "seek", "seekable", "tell", "truncate", "writable", "write",
        "writelines"
    ]
}

# Function to categorize functions and methods in a Python file
def categorize_functions_methods(file_path):
    with open(file_path, 'r') as file:
        source = file.read()

    tree = ast.parse(source)
    custom_functions, built_in_functions, methods = [], [], []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            custom_functions.append(node.name)
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
                if func_name in builtin_functions:
                    built_in_functions.append(func_name)
            elif isinstance(node.func, ast.Attribute):
                method_name = node.func.attr
                for type_name, method_list in standard_methods.items():
                    if method_name in method_list:
                        methods.append((method_name, type_name))
                        break
                else:
                    methods.append((method_name, "custom/unknown"))

    # Removing duplicates and sorting
    custom_functions = sorted(list(set(custom_functions)))
    built_in_functions = sorted(list(set(built_in_functions)))
    methods = sorted(list(set(methods)))

    return custom_functions, built_in_functions, methods

# Define the extraction directory (hard coded)
extraction_dir = '/mnt/data/extracted_files'

# Call the function for extracting the files
extract_zip_file()

# Retrieve all Python files from the extracted directory
python_files = get_python_files(extraction_dir)

# Analyzing each Python file
analysis_results = []
for file_path in python_files:
    custom, built_in, methods = categorize_functions_methods(file_path)
    analysis_results.append({
        "File Name": os.path.basename(file_path),
        "Custom Functions": ', '.join(custom),
        "Built-In Functions": ', '.join(built_in),
        "Methods and Associated Types": ', '.join([f"{m[0]} ({m[1]})" for m in methods])
    })

# Creating a DataFrame for the results
df_analysis = pd.DataFrame(analysis_results)

# Call the function to save the DataFrame as an Excel file
save_dataframe_to_excel()