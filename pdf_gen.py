#!/usr/bin/env python3

import weasyprint
# pdf = weasyprint.HTML('http://www.google.com').write_pdf()

def get_pdf(html):
    pdf = weasyprint.HTML(string=html, base_url="").write_pdf()
    return pdf
