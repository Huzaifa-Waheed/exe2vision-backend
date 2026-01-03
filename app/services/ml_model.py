import logging
from app.services.exe_to_asm import disassemble_exe

class MLModel:

    def disassemble(self, file_path):
        """
        Disassemble the given executable by calling the external exetoassembly tool.
        Returns the assembly text as a string, or an empty string on failure.
        """
        try:
            asm = disassemble_exe(file_path)
            return asm
        except Exception as e:
            logging.exception("Disassembly failed: %s", e)
            return ""

    def convert_to_rgb(self, asm):
        # TODO: implement a real asm -> image conversion; currently a placeholder
        return "image_array"

    def classify_image(self, image):
        # TODO: replace with real model inference
        return {"label": "Malware", "probability": 0.93} 
