import os
import numpy as np
import pandas as pd

# Config
MAPPING_DIR = os.getenv("NGRAMS_DIR", "NGRAMS")
OUTPUT_DIR = os.getenv("NGRAMS_OUTPUT_DIR", "./output_images")
WIDTH = int(os.getenv("NGRAM_IMAGE_WIDTH", "800"))
SLOTS_PER_LINE = int(os.getenv("NGRAM_SLOTS_PER_LINE", "16"))
DEFAULT_GRAY = (180, 180, 180)

os.makedirs(OUTPUT_DIR, exist_ok=True)

used_colors = set()
assigned_colors = {}


# Tokenization
def clean_and_tokenize_line(line: str):
    line = line.strip()
    if not line or line.startswith(";") or line.endswith(":") or line.startswith("."):
        return []
    return line.replace(",", " ").split()


def tokenize_asm_text(asm_text: str):
    tokenized = []
    for line in asm_text.splitlines():
        tokens = clean_and_tokenize_line(line)
        if tokens:
            tokenized.append(tokens)
    return tokenized


# N-grams
def extract_ngrams(tokens, n):
    if len(tokens) < n:
        return [' '.join(tokens)]
    return [' '.join(tokens[i:i+n]) for i in range(len(tokens)-n+1)]


# Load mappings
def load_all_mappings(ngram_type: str):
    color_map = {}
    try:
        for file in os.listdir(MAPPING_DIR):
            if not file.startswith(ngram_type):
                continue
            if not (file.endswith(".xlsx") or file.endswith(".csv")):
                continue

            path = os.path.join(MAPPING_DIR, file)
            try:
                df = pd.read_excel(path) if file.endswith(".xlsx") else pd.read_csv(path)
                for _, row in df.iterrows():
                    ng = str(row.iloc[0]).strip()
                    rgb = tuple(int(x) for x in str(row.iloc[1]).strip("() ").split(","))
                    if len(rgb) == 3:
                        color_map.setdefault(ng, rgb)
                        used_colors.add(rgb)
            except Exception:
                # ignore broken mapping files
                continue
    except FileNotFoundError:
        # mapping dir missing is okay — we'll assign colors dynamically
        pass

    return color_map


# Random color generator
def generate_random_unique_color():
    for _ in range(100_000):
        color = tuple(np.random.randint(0, 256, 3))
        if color not in used_colors:
            used_colors.add(color)
            return color
    return DEFAULT_GRAY


# Image generator
def generate_image(tokenized_lines, ngram_map, ngram_size):
    TOTAL_PIXELS = WIDTH * WIDTH
    pixels = np.zeros((TOTAL_PIXELS, 3), dtype=np.uint8)
    pixels[:] = DEFAULT_GRAY
    used_colors.add(DEFAULT_GRAY)

    idx = 0
    for tokens in tokenized_lines:
        ngrams = extract_ngrams(tokens, ngram_size)
        ngrams = ngrams[:SLOTS_PER_LINE]

        for ng in ngrams:
            if idx >= TOTAL_PIXELS:
                break

            if ng in ngram_map:
                color = ngram_map[ng]
            elif ng in assigned_colors:
                color = assigned_colors[ng]
            else:
                color = generate_random_unique_color()
                assigned_colors[ng] = color

            pixels[idx] = np.array(color, dtype=np.uint8)
            idx += 1

        idx += (SLOTS_PER_LINE - len(ngrams))

    return pixels.reshape((WIDTH, WIDTH, 3))


# Public API
def generate_image_from_asm_text(asm_text: str, ngram: int = 2, save_output: bool = False):
    """Return an RGB numpy array generated from assembly text."""
    global used_colors, assigned_colors
    used_colors.clear()
    assigned_colors.clear()

    if ngram not in (1, 2, 3):
        raise ValueError("ngram must be 1, 2, or 3")

    tokenized_lines = tokenize_asm_text(asm_text)
    if not tokenized_lines:
        raise RuntimeError("Assembly text is empty or invalid")

    ngram_name = {1: "unigram", 2: "bigram", 3: "trigram"}[ngram]
    ngram_map = load_all_mappings(ngram_name)

    rgb_img = generate_image(tokenized_lines, ngram_map, ngram)

    if save_output:
        import cv2
        base_name = "asm_image"
        out_path = os.path.join(OUTPUT_DIR, f"{base_name}.png")
        bgr_img = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(out_path, bgr_img)

    return rgb_img
