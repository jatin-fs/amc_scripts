import requests
import urllib3
import ssl
import PyPDF2
import json
import os
from io import BytesIO
from pdf2image import convert_from_path
import pytesseract

class CustomHttpAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_context=self.ssl_context)

def get_legacy_session():
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
    session = requests.session()
    session.mount('https://', CustomHttpAdapter(ctx))
    return session

def is_pdf_containing_text(pdf_url):
    try:
        # Download PDF
        response = get_legacy_session().get(pdf_url)
        with BytesIO(response.content) as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text = page.extract_text()
                if text.strip():  # If text is found
                    return True
        return False  # If no text found in any page
    except Exception as e:
        print(f"Error: {e}")
        return False

# OCR-based text extraction from image-based PDFs
def is_pdf_containing_text_using_ocr(pdf_url):
    try:
        # Convert PDF to images
        response = get_legacy_session().get(pdf_url)
        images = convert_from_path(BytesIO(response.content))
        
        for image in images:
            text = pytesseract.image_to_string(image)
            if text.strip():  # If text is detected
                return True
        return False  # No text detected in any image
    except Exception as e:
        print(f"Error: {e}")
        return False

# Process the filtered_data.json and update it with page count and containsText field
def process_pdf_data(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    output_data = []
    
    for obj in data:
        pdf_url = obj.get("FileUpload")
        if pdf_url:
            # Step 1: Count Pages
            try:
                response = get_legacy_session().get(pdf_url)
                with BytesIO(response.content) as pdf_file:
                    reader = PyPDF2.PdfReader(pdf_file)
                    num_pages = len(reader.pages)
            except Exception as e:
                print(f"Error downloading or processing the PDF: {e}")
                num_pages = 0

            # Step 2: Check for text in PDF
            contains_text = is_pdf_containing_text(pdf_url) or is_pdf_containing_text_using_ocr(pdf_url)

            # Step 3: Add to output
            obj["numberOfPages"] = num_pages
            obj["containsText"] = "Yes" if contains_text else "No"

            output_data.append(obj)

    # Step 4: Save the updated data to a new JSON file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(output_data, file, ensure_ascii=False, indent=4)

    print(f"Processed data saved to {output_file}")

# Input and output file paths
input_file = 'mergedresult/small_filterdata.json'  # Path to the input JSON
output_file = 'mergedresult/processed_data.json'  # Path to the output JSON

process_pdf_data(input_file, output_file)
