from datetime import datetime
from training.services.certificate import Certificate
import fitz


class Test_Cert_PDF:
    def test_creates_pdf_with_name_and_date(self):
        cert = Certificate()
        training_name = 'Purchase Training For Program Coordinators'
        pdf_bytes = cert.generate_pdf(training_name, "Molly Bloom", datetime(2023, 4, 1))

        returned_doc = fitz.open("pdf", pdf_bytes)  # type: ignore
        page = returned_doc.load_page(0)

        assert any(field.field_name == 'name' and field.field_value == 'Molly Bloom' for field in page.widgets())
        assert any(field.field_name == 'date' and field.field_value == 'April 1, 2023' for field in page.widgets())

    def test_reads_correct_pdf(self):
        cert = Certificate()
        training_name = 'Fleet Training For Program Coordinators'
        pdf_bytes = cert.generate_pdf(training_name, "Molly Bloom", datetime(2023, 4, 1))

        returned_doc = fitz.open("pdf", pdf_bytes)  # type: ignore
        page = returned_doc.load_page(0)
        text = page.get_text()

        assert "GSA SmartPay Fleet Card Training for Agency" in text
