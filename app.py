@app.route('/', methods=['GET', 'POST'])
def send_email():
    if request.method == 'POST':
        # Collect form data
        full_name = request.form['full_name']
        national_insurance = request.form['national_insurance']
        share_code = request.form['share_code']
        images = request.files.getlist('images')

        # Create email body
        body = f"Full Name: {full_name}\nNational Insurance Number: {national_insurance}\nShare Code: {share_code}"

import smtplib
        from email.message import EmailMessage

        msg = EmailMessage()
        msg['Subject'] = 'Form Submission with Attachments'
        msg['From'] = 'rqtahirtest@gmail.com'
        msg['To'] = 'rq.tahir@khuddam.co.uk'
        msg.set_content(body)

        # Attach uploaded images
        for image in images:
            if image.filename:
                file_data = image.read()
                msg.add_attachment(file_data, maintype='image', subtype='jpeg', filename=image.filename)

        # Send email using Gmail SMTP
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('rqtahirtest@gmail.com', 'Champion13!')
            smtp.send_message(msg)
