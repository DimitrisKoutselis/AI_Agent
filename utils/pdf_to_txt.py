import os
from PyPDF2 import PdfReader

def convert_pdf_to_txt(pdf_folder, txt_folder):
    os.makedirs(txt_folder, exist_ok=True)

    for filename in os.listdir(pdf_folder):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder, filename)
            txt_path = os.path.join(txt_folder, f"{os.path.splitext(filename)[0]}.txt")

            with open(pdf_path, 'rb') as pdf_file:
                pdf_reader = PdfReader(pdf_file)
                text = ''

                for page in pdf_reader.pages:
                    text += page.extract_text()

            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(text)

            print(f"Converted {filename} to {os.path.basename(txt_path)}")

if __name__ == "__main__":
    pdf_folder = os.path.join('../data', 'pdfs')
    txt_folder = os.path.join('../data', 'txts')
    convert_pdf_to_txt(pdf_folder, txt_folder)