from pdf2image import convert_from_path
from PIL import Image
import os

# Path to the PDF file
pdf_path = os.path.join(os.path.dirname(__file__), 'Dosp_vše_190513.pdf')
# Output PNG file path
output_path = os.path.join(os.path.dirname(__file__), 'Dosp_vše_190513.png')

# Convert PDF to a list of images (one per page)
images = convert_from_path(pdf_path, poppler_path=r'D:\Poppler\poppler-25.07.0\Library\bin')

# Combine all pages vertically into one image
width = max(img.width for img in images)
total_height = sum(img.height for img in images)
combined_img = Image.new('RGB', (width, total_height), color=(255,255,255))

y_offset = 0
for img in images:
    combined_img.paste(img, (0, y_offset))
    y_offset += img.height

# Save as a single PNG file
combined_img.save(output_path)
print(f'PDF converted and saved as {output_path}')

# --- PDF to text conversion ---
try:
    from PyPDF2 import PdfReader
    txt_output_path = os.path.join(os.path.dirname(__file__), 'Dosp_vše_190513.txt')
    reader = PdfReader(pdf_path)
    all_text = []
    for page in reader.pages:
        all_text.append(page.extract_text() or "")
    with open(txt_output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_text))
    print(f'PDF text extracted and saved as {txt_output_path}')
except ImportError:
    print('PyPDF2 is not installed. PDF to text conversion skipped.')
except Exception as e:
    print(f'Error extracting text from PDF: {e}')
