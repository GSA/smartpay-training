import os
import fitz

PDF_PATH = '../../data/blank_certificates'
SCRIPT_DIR = os.path.dirname(__file__)

certificates = {
    'Travel Training for Card/Account Holders and Approving Officials': 'c_ah_ao_travel.pdf',
    'Travel Training for Agency/Organization Program Coordinators': 'a_opc_travel.pdf',
    'Purchase Training for Card/Account Holders and Approving Officials': 'c_ah_ao_purchase.pdf',
    'Purchase Training For Program Coordinators': 'a_opc_purchase.pdf',
    'Fleet Training For Program Coordinators': 'a_opc_fleet.pdf'
}


class Certificate:
    def __init__(self):
        pass

    def generate_pdf(self, training_name, name, agency, date):
        date_string = '{dt:%B} {dt.day}, {dt.year}'.format(dt=date)
        data = {'name': name, 'agency': agency, 'date': date_string}
        pdf = certificates[training_name]
        empty_pdf_path = os.path.join(SCRIPT_DIR, PDF_PATH, pdf)

        doc = fitz.open(empty_pdf_path)  # type: ignore
        page = doc.load_page(0)

        for field in page.widgets():
            field_name = field.field_name
            field.text_font = 'Merriweather'
            field.field_value = data[field_name]
            # field flag of 1 corresponds to "read-only"
            field.field_flags = 1
            field.update()

        doc.need_appearances(True)
        return doc.tobytes(linear=True, deflate_fonts=True, expand=2)

    def generate_gspc_pdf(self, name, agency, date, expiration_date):
        date_string = '{dt:%B} {dt.day}, {dt.year}'.format(dt=date)
        data = {'name': name, 'agency': agency, 'date': date_string, 'expiration-date': expiration_date}
        pdf = 'c_gspc.pdf'
        empty_pdf_path = os.path.join(SCRIPT_DIR, PDF_PATH, pdf)

        doc = fitz.open(empty_pdf_path)  # type: ignore
        page = doc.load_page(0)

        for field in page.widgets():
            field_name = field.field_name
            field.text_font = 'Merriweather'
            field.field_value = data[field_name]
            # field flag of 1 corresponds to "read-only"
            field.field_flags = 1
            field.update()

        doc.need_appearances(True)
        return doc.tobytes(linear=True, deflate_fonts=True, expand=2)