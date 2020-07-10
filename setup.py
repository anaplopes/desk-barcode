import sys
from cx_Freeze import setup, Executable
import ghostscript
import PIL
import treepoem
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar
from tkinter.filedialog import askopenfilename, askdirectory


# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": []}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
icon = "icon.ico"


if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "coder",
        version = "1.0",
        description = "Gerador de códigos",
        options = {"build_exe": build_exe_options},
        executables = [Executable("interface.py", base=base, icon=icon)])