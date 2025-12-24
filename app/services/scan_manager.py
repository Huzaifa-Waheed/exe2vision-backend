import random
from app.services.file_manager import FileManager
from app.database.manager import DatabaseManager

class ScanManager:

    @staticmethod
    def process_scan(db, user, file):
        # 1️⃣ Save file to disk
        file_path = FileManager.save_file(file)

        # 2️⃣ Simulate ML scan result (replace later)
        # asm = MLModel().disassemble(file_path)
        # ngrams = MLModel().generate_ngrams(asm)
        # image = MLModel().convert_to_rgb(ngrams)
        # result = MLModel().classify_image(image)
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

