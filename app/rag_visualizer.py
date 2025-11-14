"""
RAG Visualizer Pro v3 (Stable + High-Resolution + Smart Flow)
-------------------------------------------------------------
✅ Detects flow pattern based on question, context, and answer
✅ Supports Linear, Loop, Parallel, Re-rank, and Hybrid flows
✅ Asks user: "Do you want image or flow diagram?"
✅ Auto-opens chosen output (PNG + SVG for high clarity)
✅ Logs all visualizations with timestamp
✅ Prevents 'expected string or bytes-like object' errors
✅ Generates high-resolution (300 DPI) visuals
"""

import os
import re
import sys
import platform
import subprocess
from datetime import datetime
from graphviz import Digraph

# Ensure Graphviz Path
os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"
print("✅ Graphviz path added:", r"C:\Program Files\Graphviz\bin")

# ------------------------------------------------------------
# 1️⃣ Extract RAG-related keywords
# ------------------------------------------------------------
def extract_rag_keywords(text: str):
    text = str(text or "")
    possible_keywords = [
        "query", "retriever", "vector", "database", "embedding",
        "model", "generation", "llm", "chunk", "index", "context",
        "search", "store", "retrieve", "rank", "rerank", "feedback",
        "refine", "parallel", "ensemble", "combine", "fusion", "hybrid", "cot"
    ]
    found = [kw for kw in possible_keywords if re.search(rf"\b{kw}\b", text, re.IGNORECASE)]
    return list(set(found))

# ------------------------------------------------------------
# 2️⃣ Detect flow pattern (Linear / Loop / Parallel / Rerank / Hybrid)
# ------------------------------------------------------------
def detect_flow_pattern(text: str):
    text = str(text or "").lower()
    if any(w in text for w in ["parallel", "simultaneous", "compare", "ensemble", "multi-path"]):
        return "parallel"
    elif any(w in text for w in ["loop", "feedback", "refine", "iterate", "retrain", "improve"]):
        return "loop"
    elif any(w in text for w in ["rank", "rerank", "filter", "score"]):
        return "rerank"
    elif any(w in text for w in ["hybrid", "fusion", "combine", "cross"]):
        return "hybrid"
    else:
        return "linear"

# ------------------------------------------------------------
# 3️⃣ Generate the flow diagram (300 DPI + SVG Export)
# ------------------------------------------------------------
def generate_rag_flow_diagram(keywords, pattern="linear", output_path="rag_flow"):
    dot = Digraph(comment=f"RAG {pattern.title()} Flow", format="png")

    # Global Graphviz Attributes (High Quality)
    dot.attr(
        rankdir='LR',
        dpi='300',
        size='10,6!',
        fontsize='14',
        nodesep='0.5',
        ranksep='0.75',
        fontname="Helvetica-Oblique"
    )

    # Node Definitions
    dot.node("Q", "User Query", shape="oval", color="skyblue", style="filled")
    if any(k in keywords for k in ["embedding", "model"]):
        dot.node("E", "Embedding Model", shape="box", color="lightgreen", style="filled")
    if any(k in keywords for k in ["vector", "database"]):
        dot.node("V", "Vector DB", shape="cylinder", color="lightyellow", style="filled")
    if any(k in keywords for k in ["retriever", "search", "rank", "index"]):
        dot.node("R", "Retriever", shape="box", color="lightcoral", style="filled")
    if any(k in keywords for k in ["llm", "generation"]):
        dot.node("G", "LLM Generator", shape="ellipse", color="lightgray", style="filled")
    dot.node("A", "Final Answer", shape="oval", color="lightblue", style="filled")

    # Edge Connections by Pattern
    if pattern == "linear":
        dot.attr(edgecolor="black", penwidth="1.8")
        dot.edge("Q", "E", label="embed")
        dot.edge("E", "V", label="store/search")
        dot.edge("V", "R", label="retrieve")
        dot.edge("R", "G", label="augment")
        dot.edge("G", "A", label="generate")

    elif pattern == "loop":
        dot.attr(edgecolor="blue", penwidth="2.0")
        dot.edge("Q", "E", label="embed")
        dot.edge("E", "V", label="store/search")
        dot.edge("V", "R", label="retrieve")
        dot.edge("R", "G", label="generate")
        dot.edge("G", "R", label="refine loop", color="blue")
        dot.edge("G", "A", label="finalize")

    elif pattern == "parallel":
        dot.attr(edgecolor="purple", penwidth="2.0")
        dot.edge("Q", "E", label="embedding path")
        dot.edge("Q", "R", label="retrieval path")
        dot.edge("E", "V", label="index")
        dot.edge("V", "G", label="vector merge")
        dot.edge("R", "G", label="context combine")
        dot.edge("G", "A", label="synthesize")

    elif pattern == "rerank":
        dot.attr(edgecolor="green", penwidth="2.0")
        dot.edge("Q", "R", label="initial retrieval")
        dot.edge("R", "G", label="LLM rerank")
        dot.edge("G", "A", label="final answer")

    elif pattern == "hybrid":
        dot.attr(edgecolor="orange", penwidth="2.0")
        dot.edge("Q", "E", label="embedding")
        dot.edge("Q", "R", label="symbolic retrieval")
        dot.edge("E", "V", label="semantic DB")
        dot.edge("R", "V", label="fusion")
        dot.edge("V", "G", label="context combine")
        dot.edge("G", "A", label="generate hybrid response")

    # Render PNG (High-Resolution)
    dot.render(output_path, cleanup=True)
    print(f"✅ {pattern.title()} RAG Flow Diagram generated → {output_path}.png")

    # Also Export SVG (for clarity)
    dot.format = 'svg'
    dot.render(f"{output_path}_svg", cleanup=True)
    print(f"🌐 SVG version saved → {output_path}_svg.svg")

    # Auto-open the generated PNG
    img_file = f"{output_path}.png"
    if os.path.exists(img_file):
        try:
            if platform.system() == "Windows":
                os.startfile(img_file)
            elif platform.system() == "Darwin":
                subprocess.run(["open", img_file])
            else:
                subprocess.run(["xdg-open", img_file])
            print(f"🖼️  Opened: {img_file}")
        except Exception as e:
            print(f"⚠️ Could not open image automatically: {e}")
    else:
        print(f"❌ Image not found at {img_file}")

    return f"{output_path}.png"

# ------------------------------------------------------------
# 4️⃣ Orchestrator with Interactive Choice + Safe Handling
# ------------------------------------------------------------
def visualize_from_context(context_text: str, query: str = None, answer: str = None):
    # Convert everything to strings (prevent TypeError)
    context_text, query, answer = str(context_text or ""), str(query or ""), str(answer or "")
    full_text = f"{query}\n{context_text}\n{answer}"
    keywords = extract_rag_keywords(full_text)

    if not keywords:
        print("⚠️ No relevant RAG-related terms detected.")
        return None

    pattern = detect_flow_pattern(full_text)
    print(f"🧠 Detected RAG flow pattern: {pattern.title()}")

    # Ask if user wants visualization
    choice = input("❓ Do you want to generate an image or flow diagram? (type 'y' or 'n'): ").strip().lower()
    if choice != "y":
        print("❎ Skipped diagram generation.")
        return None

    # Ask type of visualization
    visualize_output = input(
        "🖼️ Choose output type - 'image' (static view) or 'flow diagram' (interactive): "
    ).strip().lower().replace(" ", "")
    if not any(v in visualize_output for v in ["image", "flow", "diagram"]):
        print("❎ Invalid choice. Skipped diagram generation.")
        return None

    # Timestamped output name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', query[:40])
    output_dir = r"C:\Users\admin\Desktop\RAG_AI_ASSISTANT\outputs"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"rag_flow_{safe_name}_{timestamp}")

    # Generate flow
    img_path = generate_rag_flow_diagram(keywords, pattern, output_path)

    # Log the visualization
    log_file = os.path.join(output_dir, "rag_log.txt")
    with open(log_file, "a", encoding="utf-8") as log:
        log.write(f"{safe_name}_{timestamp}.png → {pattern.title()} flow [{visualize_output}]\n")

    print(f"🪶 Logged in: {log_file}")
    return img_path

# ------------------------------------------------------------
# 5️⃣ Run standalone
# ------------------------------------------------------------
if __name__ == "__main__":
    sample_question = "How does RAG handle feedback and reranking?"
    sample_context = """
    The retriever fetches documents from a vector database.
    The LLM refines responses through a feedback loop and applies reranking.
    """
    sample_answer = "RAG improves responses iteratively through reranking and feedback refinement."
    visualize_from_context(sample_context, query=sample_question, answer=sample_answer)
