import os
import traceback
from PyPDF2 import PdfReader
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def convert_pdf_to_txt(pdf_folder, txt_folder):
    """
    Convert PDF files in a folder to text files.
    Handles errors gracefully and logs issues.
    
    Args:
        pdf_folder (str): Path to folder containing PDF files
        txt_folder (str): Path to folder where text files will be saved
    """
    os.makedirs(txt_folder, exist_ok=True)
    
    for filename in os.listdir(pdf_folder):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder, filename)
            txt_path = os.path.join(txt_folder, f"{os.path.splitext(filename)[0]}.txt")
            
            logger.info(f"Converting {filename} to {os.path.basename(txt_path)}")
            
            try:
                with open(pdf_path, 'rb') as pdf_file:
                    pdf_reader = PdfReader(pdf_file)
                    text = ''
                    
                    for page_num, page in enumerate(pdf_reader.pages):
                        try:
                            page_text = page.extract_text()
                            if page_text:
                                text += page_text
                            else:
                                logger.warning(f"No text extracted from page {page_num+1} in {filename}")
                        except Exception as e:
                            logger.warning(f"Error extracting text from page {page_num+1} in {filename}: {str(e)}")
                            continue
                
                if not text.strip():
                    logger.warning(f"PyPDF2 couldn't extract text from {filename}, trying alternative method")
                    try:
                        import pdfminer
                        from pdfminer.high_level import extract_text as pdfminer_extract
                        text = pdfminer_extract(pdf_path)
                    except ImportError:
                        logger.warning("pdfminer.six not installed, skipping alternative extraction")
                        pass
                
                if text.strip():
                    with open(txt_path, 'w', encoding='utf-8') as txt_file:
                        txt_file.write(text)
                    logger.info(f"Successfully converted {filename} to {os.path.basename(txt_path)}")
                else:
                    logger.error(f"Failed to extract any text from {filename}")
                    
            except Exception as e:
                logger.error(f"Error processing {filename}: {str(e)}")
                logger.debug(traceback.format_exc())

if __name__ == "__main__":
    pdf_folder = os.path.join('../data', 'pdfs')
    txt_folder = os.path.join('../data', 'txts')
    convert_pdf_to_txt(pdf_folder, txt_folder)