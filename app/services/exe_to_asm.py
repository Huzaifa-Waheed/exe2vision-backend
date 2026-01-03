import os
import logging
import pefile
from capstone import (
    Cs,
    CS_ARCH_X86,
    CS_MODE_64,
    CS_MODE_32,
    CS_ARCH_ARM,
    CS_MODE_ARM,
    CS_ARCH_ARM64,
)


def disassemble_exe(file_path: str) -> str:
    """
    Disassemble a PE executable using `pefile` and `capstone` and return the assembly text.

    Returns the assembly as a string (may be empty if no executable sections are found).
    Raises RuntimeError on invalid PE or unsupported architecture.
    """
    try:
        with open(file_path, "rb") as f:
            file_bytes = f.read()

        # Basic PE check
        if not file_bytes.startswith(b"MZ"):
            logging.error("File is not a valid PE: %s", file_path)
            raise RuntimeError("Not a valid PE file")

        pe = pefile.PE(data=file_bytes)

        # Architecture mapping
        machine_map = {
            0x8664: (CS_ARCH_X86, CS_MODE_64),
            0x14c:  (CS_ARCH_X86, CS_MODE_32),
            0x1c0:  (CS_ARCH_ARM, CS_MODE_ARM),
            0xaa64: (CS_ARCH_ARM64, 0),
        }

        machine = pe.FILE_HEADER.Machine
        if machine not in machine_map:
            logging.error("Unsupported architecture 0x%02x for file %s", machine, file_path)
            raise RuntimeError(f"Unsupported architecture: 0x{machine:x}")

        cs_arch, cs_mode = machine_map[machine]
        md = Cs(cs_arch, cs_mode)

        asm_code = ""

        # Disassemble executable sections only
        for section in pe.sections:
            # IMAGE_SCN_MEM_EXECUTE = 0x20000000
            if not section.Characteristics & 0x20000000:
                continue  # skip non-executable sections

            section_data = section.get_data()
            if not section_data:
                continue

            # Use the section's virtual address for disassembly offsets
            vaddr = section.VirtualAddress
            try:
                for instr in md.disasm(section_data, vaddr):
                    asm_code += f"{instr.mnemonic} {instr.op_str}\n"
            except Exception:
                # be tolerant of disassembly errors in a section
                logging.exception("Error disassembling section %s of %s", section.Name, file_path)
                continue

        return asm_code

    except pefile.PEFormatError as e:
        logging.exception("PE parsing failed for %s: %s", file_path, e)
        raise RuntimeError("Invalid PE file") from e
    except Exception as e:
        logging.exception("Disassembly failed for %s: %s", file_path, e)
        raise
