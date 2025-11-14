import os
import fitz  # PyMuPDF
from paddleocr import PaddleOCR
import json
from tqdm import tqdm

# === Configuration ===
INPUT_PDF = "input/mastering_rag.pdf"
OUTPUT_DIR = "data/hybrid_output"
CLEAN_TEXT_PATH = "input/clean_text.txt"

# Initialize PaddleOCR (CPU mode)
ocr = PaddleOCR(use_angle_cls=True, lang="en", use_gpu=False, show_log=False)

# Ensure output folder exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_text_from_page(image_path):
    """Run full-page OCR on a given image."""
    result = ocr.ocr(image_path)
    lines = []
    if result and result[0]:
        for line in result[0]:
            lines.append(line[1][0])
    return " ".join(lines)

def hybrid_extract():
    """Main extraction logic combining structure + full-page OCR."""
    doc = fitz.open(INPUT_PDF)
    all_text = []

    for page_num in tqdm(range(len(doc)), desc="Extracting Pages", unit="page"):
        try:
            # Render the page to an image
            page = doc[page_num]
            pix = page.get_pixmap(dpi=300)
            page_img_path = os.path.join(OUTPUT_DIR, f"page_{page_num+1}.png")
            pix.save(page_img_path)

            # --- Step 1: Try PaddleOCR Structure (Layout-aware) ---
            structure_res = ocr.ocr(page_img_path, cls=True)

            if structure_res and len(structure_res[0]) > 0:
                text_segments = [line[1][0] for line in structure_res[0]]
                combined_text = " ".join(text_segments)
                all_text.append(combined_text)
                print(f"[✔] Structured OCR extracted page {page_num+1}")
            else:
                # --- Step 2: Fallback to Full-Page OCR ---
                fallback_text = extract_text_from_page(page_img_path)
                if fallback_text.strip():
                    all_text.append(fallback_text)
                    print(f"[🩵] Fallback OCR used for page {page_num+1}")
                else:
                    print(f"[⚠️] No text found on page {page_num+1}")

        except Exception as e:
            print(f"[⚠️] Error processing page {page_num+1}: {e}")
            continue

    # Save combined clean text
    os.makedirs(os.path.dirname(CLEAN_TEXT_PATH), exist_ok=True)
    with open(CLEAN_TEXT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(all_text))

    print(f"\n✅ Hybrid extraction completed successfully!")
    print(f"📄 Text saved to: {CLEAN_TEXT_PATH}")
    print(f"🧩 Total pages processed: {len(doc)}")

if __name__ == "__main__":
    hybrid_extract()
