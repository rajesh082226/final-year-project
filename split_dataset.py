import os
import shutil
import random

RAW_DIR = "raw_data"
OUTPUT_DIR = "dataset"

CLASSES = ["fire", "no_fire"]
SPLIT = (0.7, 0.15, 0.15)  # train, validation, test

random.seed(42)

for cls in CLASSES:
    src_dir = os.path.join(RAW_DIR, cls)

    if not os.path.exists(src_dir):
        raise FileNotFoundError(f"❌ Folder not found: {src_dir}")

    files = os.listdir(src_dir)
    random.shuffle(files)

    total = len(files)
    train_end = int(total * SPLIT[0])
    val_end = train_end + int(total * SPLIT[1])

    splits = {
        "train": files[:train_end],
        "validation": files[train_end:val_end],
        "test": files[val_end:]
    }

    for split, split_files in splits.items():
        dest_dir = os.path.join(OUTPUT_DIR, split, cls)
        os.makedirs(dest_dir, exist_ok=True)

        for file in split_files:
            shutil.copy(
                os.path.join(src_dir, file),
                os.path.join(dest_dir, file)
            )

print("✅ Dataset split into train / validation / test successfully")
