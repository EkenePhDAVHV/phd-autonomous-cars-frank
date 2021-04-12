from fpdf import FPDF


class PDFDocumenter(FPDF):

    def titles(self):
        self.set_xy(0.0, 0.0)
        self.set_font('Times', 'B', 16)
        self.cell(w=210.0, h=40.0, align='C', txt="", border=0)
