import requests
import urllib3
import ssl
import PyPDF2
import os
import json
from io import BytesIO

# Custom HTTP Adapter to handle legacy SSL connection
class CustomHttpAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_context=self.ssl_context)

# Create legacy session for SSL connection
def get_legacy_session():
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
    session = requests.session()
    session.mount('https://', CustomHttpAdapter(ctx))
    return session

# Function to get number of pages from PDF URL
def get_pdf_page_count(pdf_url, download_path="temp.pdf"):
    try:
        # Make the request to download the PDF
        response = get_legacy_session().get(pdf_url)

        # Check if the content is a PDF
        content_type = response.headers.get('Content-Type', '')
        if 'pdf' not in content_type.lower():
            print(f"Warning: The content is not a PDF, content type is: {content_type}")
            return None

        # Ensure the response was successful
        if response.status_code != 200:
            print(f"Failed to download the PDF. HTTP Status Code: {response.status_code}")
            return None

        # Save the file to disk first
        with open(download_path, 'wb') as f:
            f.write(response.content)

        # Now, read the saved PDF
        with open(download_path, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            return len(reader.pages)
    
    except Exception as e:
        print(f"Error downloading or processing the PDF: {e}")
        return None
    finally:
        # Clean up: delete the downloaded file after processing
        if os.path.exists(download_path):
            os.remove(download_path)

# Load the filtered_data.json file from the mergedresult folder
filtered_data_file = "mergedresult/small_filterdata.json"
output_file = "mergedresult/small_filtered_with_pages.json"

try:
    with open(filtered_data_file, "r", encoding="utf-8") as file:
        filtered_data = json.load(file)

    # Add the numberOfPages field for each object
    for item in filtered_data:
        pdf_url = item.get("FileUpload")
        if pdf_url:
            num_pages = get_pdf_page_count(pdf_url)
            if num_pages is not None:
                item["numberOfPages"] = num_pages
            else:
                item["numberOfPages"] = "Error"

    # Save the updated data to a new JSON file
    with open(output_file, "w", encoding="utf-8") as outfile:
        json.dump(filtered_data, outfile, ensure_ascii=False, indent=4)

    print(f"Updated data with page numbers saved to {output_file}")

except Exception as e:
    print(f"Error occurred: {e}")
