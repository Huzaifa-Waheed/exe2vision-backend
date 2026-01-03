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
