import os
import stat
import shutil
import zipfile
import subprocess
import sys
import urllib.request

def remove_directory(directory):
    if os.path.exists(directory):
        def set_rw(operation, name, exc):
            os.chmod(name, stat.S_IWRITE)
            return True
        shutil.rmtree(directory, onerror=set_rw)
        shutil.rmtree(directory, ignore_errors=True)

def remove(file_or_directory_path):
    if os.path.exists(file_or_directory_path):
        if os.path.isfile(file_or_directory_path):
            os.remove(file_or_directory_path)
        else:
            remove_directory(file_or_directory_path)

def unzip_folder(zip_file: zipfile.ZipFile, folder_in_zip: str, dest_on_disk: str):
    zip_file_names = zip_file.namelist()
    file_names_to_extract = []
    for file_member in zip_file_names:
        file_name = str(file_member)
        if file_name.startswith(folder_in_zip) and file_name != folder_in_zip:
            file_names_to_extract.append(file_name)
    zip_file.extractall(dest_on_disk, file_names_to_extract)

def download_page(url: str) -> str:
    return urllib.request.urlopen(url).read().decode('utf-8')

def execute_command(command_string: str, expected_ret_code: int = 0, print_command: bool = True):
    if print_command:
        print(f"Executing: {command_string}")
    process = subprocess.run(args=command_string, shell=True, cwd=os.getcwd())
    if process.returncode != expected_ret_code:
        raise Exception(f"Expected return code: {expected_ret_code} is diffrent from actual: {process.returncode}")

def add_exec_flag_if_linux(file_path):
    if is_linux():
        file_stat = os.stat(file_path)
        os.chmod(file_path, file_stat.st_mode | stat.S_IEXEC)

def is_windows():
    return sys.platform.startswith('win')

def is_linux():
    return is_windows() == False

def get_path_separator():
    return ';' if is_windows() else ':'
