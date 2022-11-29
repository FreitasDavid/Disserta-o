import sys
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from time import sleep
from glob import glob

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

if __name__ == '__main__':
    print('Iniciando envio')
    for arg in sys.argv:
        if '-u=' in arg:
            user = arg.split('=')[-1]
        elif '-p=' in arg:
            password = arg.split('=')[-1]
        elif '-s=' in arg:
            send_to = arg.split('=')[-1]

    subject = '[Resultados - ELO Clubes]'
    body = 'Seguem resultados.'
    attachments = glob('results_*.txt')
    print('Arquivo selecionado')
    enviado = False
    tentativas = 0
    print('Enviando')
    while not enviado or tentativas < 10:
        try:
            send(user, password, send_to, subject, body, attachments)
            enviado = True
        except Exception as e:
            print(f'Falhou: {e}')
            tentativas += 1
            sleep(5)
            print('Tentando novamente')