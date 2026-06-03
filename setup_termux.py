import os
import sys
import shutil
import subprocess

def compile_termux():
    print("="*60)
    print("            TERMUX COMPILATION & SETUP SCRIPT")
    print("="*60)
    
    # 1. Update Termux pkg and install dependencies
    print("\n[1/5] Installing Termux system dependencies (clang, make, python)...")
    try:
        # Run pkg commands to install clang compiler and make utilities
        subprocess.check_call("pkg update -y", shell=True)
        subprocess.check_call("pkg install -y clang make python", shell=True)
    except Exception as e:
        print(f"Warning: System packages installation failed or skipped (may already be installed): {e}")

    # 2. Install Cython
    print("\n[2/5] Installing Python modules (cython) via pip...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "cython"])
    except Exception as e:
        print(f"Error installing Python packages: {e}")
        sys.exit(1)

    # 3. Create cython setup file
    print("\n[3/5] Generating Cython configuration...")
    setup_content = """from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("app.py", compiler_directives={'language_level': "3"})
)
"""
    with open("setup_build.py", "w") as f:
        f.write(setup_content)

    # 4. Compile app.py
    print("\n[4/5] Compiling app.py to machine binary (.so) file...")
    try:
        subprocess.check_call([sys.executable, "setup_build.py", "build_ext", "--inplace"])
        print("Compilation successful!")
    except Exception as e:
        print(f"Compilation failed: {e}")
        if os.path.exists("setup_build.py"):
            os.remove("setup_build.py")
        sys.exit(1)

    # 5. Clean up temporary files & original app.py
    print("\n[5/5] Performing secure cleanup of source files...")
    
    # Remove setup_build.py
    if os.path.exists("setup_build.py"):
        os.remove("setup_build.py")
        
    # Remove intermediate app.c
    if os.path.exists("app.c"):
        os.remove("app.c")
        
    # Remove build directory
    if os.path.exists("build") and os.path.isdir("build"):
        shutil.rmtree("build")
        
    # Crucial step: Remove app.py (the raw source code)
    if os.path.exists("app.py"):
        os.remove("app.py")
        print("SUCCESS: Original app.py source code has been permanently deleted!")

    print("\n" + "="*50)
    print("TERMUX COMPILATION COMPLETE & SECURED!")
    print("The code is now compiled into native binary machine code.")
    print("Mangers cannot read or decompile the source files.")
    print("\nTo start the broadcaster, run:")
    print("    python run.py")
    print("="*50)

if __name__ == "__main__":
    compile_termux()
