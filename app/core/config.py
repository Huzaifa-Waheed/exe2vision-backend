from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
# Path to the external exetoassembly tool (can be an absolute path or executable on PATH)
EXE_TO_ASM_PATH = os.getenv("EXE_TO_ASM_PATH", "exetoassembly")
# Timeout (seconds) for the external exetoassembly process
EXE_TO_ASM_TIMEOUT = int(os.getenv("EXE_TO_ASM_TIMEOUT", "30"))
