from flask import Flask, request, render_template_string
import smtplib
from email.message import EmailMessage
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# HTML form template
form_template = '''
<!doctype html>
<title>Send Email with Attachments</title>
<h2>Send Email with Attachments</h2>
<form method=post enctype=multipart/form-data>
  Full Name: <input type=text name=full_name><br><br>
  National Insurance Number: <input type=text name=national_insurance><br><br>
  Share Code: <input type=text name=share_code><br><br>
  Attach Images: <input type=file name=images multiple><br><br>
  <input type=submit value=Send>
</form>
'''

@app.route('/', methods=['GET', 'POST'])
def send_email():
    if request.method == 'POST':
        full_name = request.form['full_name']
        national_insurance = request.form['national_insurance']
        share_code = request.form['share_code']
        images = request.files.getlist('images')

        # Create the email message
        msg = EmailMessage()
        msg['Subject'] = 'Form Submission with Attachments'
        msg['From'] = 'rqtahirtest@gmail.com'  # Replace with your Gmail
        msg['To'] = 'info@kendall.com'
        body = f"Full Name: {full_name}\nNational Insurance Number: {national_insurance}\nShare Code: {share_code}"
        msg.set_content(body)

        # Save and attach images
        for image in images:
            if image.filename:
                filename = secure_filename(image.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(filepath)
                with open(filepath, 'rb') as f:
                    file_data = f.read()
                    msg.add_attachment(file_data, maintype='image', subtype='jpeg', filename=filename)

        # Send the email using Gmail SMTP
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('rqtahirtest@gmail.com', 'Champion13!')  # Replace with your Gmail App Password
            smtp.send_message(msg)

        return 'Email sent successfully!'

    return render_template_string(form_template)

if __name__ == '__main__':
    app.run(debug=True)
