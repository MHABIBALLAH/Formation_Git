import sys
import os
# Add src to path to allow importing our modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.ocr.reader import extract_text_from_image

if __name__ == "__main__":
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        if not os.path.exists(image_path):
            print(f"Error: Image file not found at '{image_path}'")
            sys.exit(1)

        text = extract_text_from_image(image_path)
        print("--- OCR Output ---")
        print(text)
        print("--------------------")
    else:
        print("Usage: python scripts/run_ocr.py <path_to_image>")
        sys.exit(1)
