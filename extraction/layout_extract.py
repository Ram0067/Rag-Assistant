import os
import fitz
from paddleocr import PPStructure, save_structure_res
import cv2

INPUT_PDF = "input/mastering_rag.pdf"
OUTPUT_DIR = "data/structure_output"
FINAL_TEXT = "data/extracted_text.txt"

def extract():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    table_engine = PPStructure(show_log=False, lang="en")
    doc = fitz.open(INPUT_PDF)
    all_text = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        pix = page.get_pixmap(dpi=180)
        img_path = f"{OUTPUT_DIR}/page_{page_num+1}.png"
        pix.save(img_path)

        img = cv2.imread(img_path)
        result = table_engine(img)

        save_structure_res(result, OUTPUT_DIR, f"page_{page_num+1}")

        for block in result:
            if block["type"] == "text":
                lines = [line.get("text", "").strip() for line in block["res"]]
                all_text.append(" ".join(lines))

            elif block["type"] == "table" and "res" in block:
                table_rows = []
                for row in block["res"]:
                    row_text = [cell.get("text", "").strip() for cell in row]
                    table_rows.append(" | ".join(row_text))
                all_text.append("\n".join(table_rows))

        print(f"[✔] Processed Page {page_num+1}/{len(doc)}")

    with open(FINAL_TEXT, "w", encoding="utf-8") as f:
        f.write("\n\n".join(all_text))

    print("\n✅ Extraction Complete →", FINAL_TEXT)

if __name__ == "__main__":
    extract()
