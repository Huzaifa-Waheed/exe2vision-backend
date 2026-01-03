Hey buddy, This backend is implemented by Huzaifa. 🤷‍♂️🐱‍🚀😉😜

## exetoassembly integration 🔧

This project supports using an external `exetoassembly` tool to disassemble uploaded executables into assembly text. To enable it:

- Place the `exetoassembly` executable in your PATH or set `EXE_TO_ASM_PATH` in your environment to point to the executable.
- You can also set `EXE_TO_ASM_TIMEOUT` (seconds) to control the process timeout (default: 30).

Behavior:
- The app will call the external tool during the scan pipeline, pass the resulting assembly to `MLModel.convert_to_rgb`, then to `MLModel.classify_image`.
- If the external tool fails (not found, error or timeout), the pipeline falls back to a randomized benign/malware result.

Example (Windows PowerShell):

```powershell
# put exetoassembly.exe next to the project or somewhere on PATH
$env:EXE_TO_ASM_PATH = "C:\tools\exetoassembly.exe"
$env:EXE_TO_ASM_TIMEOUT = "30"
```

---

## Installation notes (Windows)

If pip attempts to build packages like NumPy from source and fails with a compiler error, try one of the following:

- Upgrade pip, setuptools and wheel, then prefer binary wheels:

```powershell
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt --prefer-binary
```

- Use conda/miniconda (recommended on Windows) to get prebuilt binaries:

```powershell
conda create -n exe2env python=3.11
conda activate exe2env
conda install numpy pandas opencv
pip install -r requirements.txt --no-deps
```

- If you must build from source, install the **Build Tools for Visual Studio** (C++ workload) and retry `pip install -r requirements.txt`.

Note: `requirements.txt` pins NumPy to `numpy>=1.23,<2` to prefer stable prebuilt wheels for most Python versions. If you still run into issues, run `python -V` and share the output so I can recommend a specific NumPy wheel to install.

