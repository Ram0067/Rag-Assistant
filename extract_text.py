import fitz, os, re

os.makedirs("text_clean", exist_ok=True)

doc = fitz.open("data/mastering_rag.pdf")  # <-- Use original PDF
all_text = ""

for i, page in enumerate(doc):
    text = page.get_text("text")
    text = re.sub(r"\n\s*\n", "\n\n", text)  # normalize whitespace
    all_text += text + "\n\n"

open("text_clean/full_document.txt", "w", encoding="utf8").write(all_text)

print("[DONE] Text extracted → text_clean/full_document.txt")
