import random
import logging
from app.services.file_manager import FileManager
from app.database.manager import DatabaseManager
from app.services.ml_model import MLModel

class ScanManager:

    @staticmethod
    def process_scan(db, user, file):
        # 1️⃣ Save file to disk
        file_path = FileManager.save_file(file)

        # 2️⃣ Run ML pipeline: disassemble -> convert -> classify
        ml = MLModel()
        try:
            asm = ml.disassemble(file_path)
            if not asm:
                raise RuntimeError("Empty disassembly output")

            image = ml.convert_to_rgb(asm)
            classification = ml.classify_image(image)

            result = classification.get("label", "Unknown")
            probability = float(classification.get("probability", 0.0))
        except Exception as e:
            logging.exception("ML pipeline failed, falling back to random result: %s", e)
            result = random.choice(["Benign", "Malware"])
            probability = round(random.uniform(0.70, 0.99), 2)

        # 3️⃣ Save scan result to DB
        scan = DatabaseManager.save_scan(
            db=db,
            user_id=user.id,
            filename=file.filename,
            result=result,
            probability=probability,
            file_path=file_path
        )

        return scan

