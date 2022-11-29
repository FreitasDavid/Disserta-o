import os
import sys
import email
import imaplib
import numpy as np

if __name__ == '__main__':
    username = sys.argv[-2].split('=')[-1]
    password = sys.argv[-1].split('=')[-1]
    server = 'imap.gmail.com'
    mail = imaplib.IMAP4_SSL(server)
    mail.login(username, password)
    mail.select('inbox')
    data = mail.search(None, 'ALL')
    mail_ids = data[1]
    id_list = mail_ids[0].split()   
    latest_email_id = int(id_list[-1])
    for i in range(latest_email_id + 1):
        data = mail.fetch(str(i), '(RFC822)')
        for response_part in data:
            arr = response_part[0]
            if isinstance(arr, tuple):
                try:
                    msg = email.message_from_string(str(arr[1], 'utf-8'))
                except UnicodeDecodeError:
                    msg = email.message_from_string(str(arr[1], 'latin-1'))
                
                email_subject = msg['subject']
                if '[Resultados - ELO Clubes]' not in email_subject:
                    break
                        
                for part in msg.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue
                    fileName = part.get_filename()
                    if bool(fileName):
                        filePath = os.path.join(os.getcwd(), fileName)
                        if not os.path.isfile(filePath) :
                            fp = open(filePath, 'wb')
                            fp.write(part.get_payload(decode = True))
                            fp.close()
