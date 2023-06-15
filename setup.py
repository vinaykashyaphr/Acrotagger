from cx_Freeze import setup, Executable

base = None
#if sys.platform == "win32":
#    base = "Win32GUI"

executables = [Executable("acrolauncher.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {    
        'packages':packages,
    },
}

setup(
    name = "Acrolauncher",
    options = options,
    version = "1.0",
    description = '',
    executables = executables
)