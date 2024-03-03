from flask import Flask, render_template, request
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


from flask import Flask, render_template, request
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from flask import Flask, render_template, make_response
from weasyprint import HTML

app = Flask(__name__)


def create_pdf(data, filename):
    # Load the Jinja2 environment
    # env = Environment(loader=FileSystemLoader('.'))
    
    # # Render the HTML template with the provided data
    # template = env.get_template('templates/newpdf.html')
    # html_content = template.render(email=data['email'], name=data['name'], 
    #                        start_date=data['start_date'], end_date=data['end_date'])
    
    # # Convert HTML to PDF
    # pdf_content = HTML(string=html_content).write_pdf()

    # # Create response
    # response = make_response(pdf_content)
    # response.headers['Content-Type'] = 'application/pdf'
    # response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

    # return response


    rendered_html = render_template('newpdf.html',email=data['email'], name=data['name'], 
                           start_date=data['start_date'], end_date=data['end_date'])

    # Convert rendered HTML to PDF using WeasyPrint
    pdf_content = HTML(string=rendered_html).write_pdf()
    # to save the pdf
    with open(data['email']+'.pdf', 'wb') as f:
        f.write(pdf_content)


    # Create response
    response = make_response(pdf_content)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

    return response


    
def send_email_attachment(To, subject, message, data):
    msg = MIMEMultipart()
    sender = 'iammaitreyee1@gmail.com'
    msg['From'] = sender
    msg['To'] = To
    msg['Subject'] = subject
    file_name = To + '.pdf'
    create_pdf(data, file_name)
    msg.attach(MIMEText(message))
    filename = file_name
    path = os.path.join(os.getcwd(), filename)
    with open(path, 'rb') as f:
        attachment = MIMEApplication(f.read(), _subtype='pdf')
        attachment.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(attachment)
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'iammaitreyee1@gmail.com'
    smtp_password = 'oyxdqxguccbiubuz'

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender, To, msg.as_string())

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        data = {
            'email': email,
            'name': name,
            'start_date': start_date,
            'end_date': end_date
        }
        send_email_attachment(email, 'Your PDF Attachment', 'Please find attached PDF', data)
        return 'Email sent successfully!'
    return render_template('index.html')
@app.route('/pdf',methods=['GET'])
def pdfmaker():
    return render_template('newpdf.html',email='abc@gmail.com',name='abc',start_date='2024-02-06', end_date='2024-05-06')


@app.route("/pdfa")
def aa():
    # Render your HTML template
    data={}
    data["email"]="gokulakrishnanm1998@gmail.com"
    data["name"]="Gokulakrishnan"
    data["start_date"]="2024-02-06"
    data["end_date"]="2024-05-06"
    env = Environment(loader=FileSystemLoader('.'))
    
    # Render the HTML template with the provided data
    template = env.get_template('templates/newpdf.html')
    html_content = template.render(email=data['email'], name=data['name'], 
                            start_date=data['start_date'], end_date=data['end_date'])


    rendered_html = render_template('index.html')

    # Convert rendered HTML to PDF using WeasyPrint
    pdf_content = HTML(string=rendered_html).write_pdf()

    # Create response
    response = make_response(pdf_content)

    return response


@app.route('/abc')
def indexa():
    # Render your HTML template
    rendered_html = render_template('aa.html',name="gokul")

    # Convert rendered HTML to PDF using WeasyPrint
    pdf_content = HTML(string=rendered_html).write_pdf()
    # to save the pdf
    with open('output.pdf', 'wb') as f:
        f.write(pdf_content)


    # Create response
    response = make_response(pdf_content)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

    return response

if __name__ == '__main__':
    app.run(debug=True)
