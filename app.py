# app.py

from flask import Flask, render_template, make_response
from weasyprint import HTML

app = Flask(__name__)

@app.route('/')
def bla():
    return "bla"

@app.route('/pdf')
def index():
    # Render your HTML template
    rendered_html = render_template('index.html')

    # Convert rendered HTML to PDF using WeasyPrint
    pdf_content = HTML(string=rendered_html).write_pdf()

    # Create response
    response = make_response(pdf_content)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

    return response

if __name__ == '__main__':
    app.run(debug=True)
