import requests
import urllib3
import ssl
import PyPDF2
import os
import json
import pytesseract
from io import BytesIO
from pdf2image import convert_from_bytes
from langdetect import detect

# Custom HTTP adapter for legacy SSL
class CustomHttpAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_context=self.ssl_context
        )

# SSL Session
def get_legacy_session():
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
    session = requests.session()
    session.mount('https://', CustomHttpAdapter(ctx))
    return session

# Function to detect language
def detect_language(text):
    try:
        detected_lang = detect(text)
        if detected_lang in ["gu", "hi", "en"]:
            return detected_lang
        return "Other"
    except Exception:
        return "Error"

# Function to extract text from PDF using PyPDF2
def extract_text_from_pdf(pdf_bytes):
    try:
        reader = PyPDF2.PdfReader(BytesIO(pdf_bytes))
        num_pages = len(reader.pages)

        extracted_text = ""
        for page in reader.pages:
            extracted_text += page.extract_text() or ""

        contains_text = bool(extracted_text.strip())
        return extracted_text, contains_text, num_pages

    except Exception as e:
        print(f"Error processing PDF: {e}")
        return "", False, None

# Function to extract text from images (OCR)
def extract_text_from_images(pdf_bytes):
    try:
        images = convert_from_bytes(pdf_bytes)
        ocr_text = ""
        for img in images:
            ocr_text += pytesseract.image_to_string(img, lang="eng+guj+hin")

        return ocr_text.strip()
    except Exception as e:
        print(f"Error in OCR: PDF contains images, unable to extract text. Details: {e}")
        return ""

# Main function to process PDFs
def get_pdf_details(pdf_url):
    try:
        response = get_legacy_session().get(pdf_url, timeout=15)
        pdf_bytes = response.content

        # Extract text using PyPDF2
        text, contains_text, num_pages = extract_text_from_pdf(pdf_bytes)

        if not contains_text:
            # Perform OCR if text extraction fails
            text = extract_text_from_images(pdf_bytes)
            contains_text = bool(text.strip())

        # Detect language only if text exists
        detected_language = detect_language(text) if contains_text else "Unknown"

        return {
            "numberOfPages": num_pages,
            "containsText": "yes" if contains_text else "no",
            "language": detected_language
        }

    except Exception as e:
        print(f"Error processing {pdf_url}: {e}")
        return {"numberOfPages": None, "containsText": "error", "language": "error"}

# Load filtered_data.json
with open("result_data/filtered_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Process each entry
for entry in data:
    pdf_url = entry.get("FileUpload")
    if pdf_url:
        pdf_details = get_pdf_details(pdf_url)
        entry.update(pdf_details)

# Save updated JSON
output_file = "result_data/language_data.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Updated JSON saved as {output_file}")
