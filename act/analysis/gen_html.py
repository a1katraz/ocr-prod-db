from yattag import Doc, indent
import os
#import pdfkit
from pyvirtualdisplay import Display

cwd = os.getcwd()

doc, tag, text = Doc().tagtext()

doc.asis('<!DOCTYPE html>')

with tag('html'):
    with tag('body', id = 'hello'):
        with tag('h1'):
            text('Hello World!')
        with tag('div', id='photo-container'):
            doc.stag('img', src='http://localhost'+cwd+'images/caste_charts/cst_01.png', klass="photo")
        with tag('table', klass='all-pr'):
            with tag('tr'):
                with tag('td'):
                    text('MS1')
                with tag('td'):
                    text('MS2')
                with tag('td'):
                    text('MS3')
            with tag('tr'):
                with tag('td'):
                    text('MT1')
                with tag('td'):
                    text('MT2')
                with tag('td'):
                    text('MT3')
            
with open("index.html", "w") as index:
    index.write(indent(doc.getvalue(), indent_text = True))

#display = Display(visible=0, size=(1360,768))
#display.start()

#config = pdfkit.configuration(wkhtmltopdf="/usr/bin/wkhtmltopdf")
#pdfkit.from_url('google.com', 'out.pdf', configuration=config)