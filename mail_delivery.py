import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send(from_mail, password, to_mail, subject, body, attachments = None):
    msg = MIMEMultipart()
    msg['From'] = from_mail
    msg['To'] = to_mail
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    if attachments is not None:
        for attachment_file in attachments:
            attachment = open(attachment_file, 'rb')
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename = attachment_file)
            msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(from_mail, password)
    text = msg.as_string()
    server.sendmail(from_mail, to_mail, text)
    server.quit()