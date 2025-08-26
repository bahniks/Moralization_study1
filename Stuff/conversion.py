
from pdf2image import convert_from_path
from PIL import Image
import os

menus_dir = os.path.join(os.path.dirname(__file__), 'Menus')
poppler_path = r'D:\Poppler\poppler-25.07.0\Library\bin'  # Update if needed

try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None

for filename in os.listdir(menus_dir):
    if filename.lower().endswith('.pdf'):
        pdf_path = os.path.join(menus_dir, filename)
        base_name = os.path.splitext(filename)[0]
        output_png = os.path.join(menus_dir, base_name + '.png')
        output_txt = os.path.join(menus_dir, base_name + '.txt')

        # Convert PDF to PNG
        try:
            images = convert_from_path(pdf_path, poppler_path=poppler_path)
            width = max(img.width for img in images)
            total_height = sum(img.height for img in images)
            combined_img = Image.new('RGB', (width, total_height), color=(255,255,255))
            y_offset = 0
            for img in images:
                combined_img.paste(img, (0, y_offset))
                y_offset += img.height
            combined_img.save(output_png)
            print(f'{filename} converted and saved as {output_png}')
        except Exception as e:
            print(f'Error converting {filename} to PNG: {e}')

        # Convert PDF to TXT
        if PdfReader:
            try:
                reader = PdfReader(pdf_path)
                all_text = []
                for page in reader.pages:
                    all_text.append(page.extract_text() or "")
                with open(output_txt, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(all_text))
                print(f'{filename} text extracted and saved as {output_txt}')
            except Exception as e:
                print(f'Error extracting text from {filename}: {e}')
        else:
            print('PyPDF2 is not installed. PDF to text conversion skipped.')
