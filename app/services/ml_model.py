import logging
import numpy as np
from app.services.exe_to_asm import disassemble_exe
from app.services.asm_to_image import generate_image_from_asm_text

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
        """
        Convert assembly text into an RGB image array (numpy ndarray).
        """
        try:
            # default to unigrams; you can parameterize this later
            img = generate_image_from_asm_text(asm, ngram=1, save_output=False)
            # ensure a numpy array output
            return np.asarray(img)
        except Exception as e:
            logging.exception("convert_to_rgb failed: %s", e)
            return np.zeros((800, 800, 3), dtype=np.uint8)

    def classify_image(self, image):
        # TODO: replace with real model inference
        return {"label": "Malware", "probability": 0.93} 
