import os

INPUT_DIR = "data/structure_output"
OUTPUT_FILE = "input/extracted_text.txt"

def merge_texts():
    all_text = []

    # walk through all folders and collect text
    for root, dirs, files in os.walk(INPUT_DIR):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read().strip()
                    if text:
                        all_text.append(text)

    # save merged content
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write("\n\n".join(all_text))

    print(f"✅ Merged text saved → {OUTPUT_FILE}")

if __name__ == "__main__":
    merge_texts()
