import os
import fitz

PDF_PATH = '../../data/blank_certificates'
SCRIPT_DIR = os.path.dirname(__file__)

certificates = {
    'Travel Training for Card/Account Holders and Approving Officials': 'a_opc_travel.pdf'
    # other certs go here. maybe we can have a better way to link each training to each cert
}


class Certificate:
    def __init__(self):
        pass

    def generate_pdf(self, training_name, name, date):
        data = {'name': name, 'date': date.strftime('%B %d, %Y')}
        pdf = certificates[training_name]
        empty_pdf_path = os.path.join(SCRIPT_DIR, PDF_PATH, pdf)

        doc = fitz.open(empty_pdf_path)  # type: ignore
        page = doc.load_page(0)

        for field in page.widgets():
            field_name = field.field_name
            field.text_font = 'Arial,Bold'
            field.field_value = data[field_name]
            field.field_flags = 1
            field.update()

        doc.need_appearances(True)
        return doc.tobytes(linear=True, deflate_fonts=True, expand=2)
