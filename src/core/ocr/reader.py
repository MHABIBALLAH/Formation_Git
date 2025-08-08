from PIL import Image
import pytesseract

def extract_text_from_image(image_path: str) -> str:
    """
    Extracts text from an image file using Tesseract OCR.

    Args:
        image_path: The path to the image file.

    Returns:
        The extracted text as a string.
        Returns an empty string if the file is not found or an error occurs.
    """
    try:
        with Image.open(image_path) as img:
            # Specify the language 'fra' for French
            text = pytesseract.image_to_string(img, lang='fra')
            return text
    except FileNotFoundError:
        # In a real application, you might want to log this error
        print(f"Error: The file at {image_path} was not found.")
        return ""
    except Exception as e:
        # Log other potential errors
        print(f"An error occurred during OCR processing: {e}")
        return ""
