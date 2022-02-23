from PyPDF2 import PdfFileReader, PdfFileWriter

def extract_pdf_text(file_path: str):
    pdf = PdfFileReader(file_path)

    file_name = file_path.split('.')[0]
    with open(f'{file_name}.txt', 'w') as f:
        for page_num in range(pdf.numPages):
            print(f'Page: {page_num}')
            page_obj = pdf.getPage(page_num)
