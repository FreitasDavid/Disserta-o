from glob import glob

import sys
from mail_delivery import *

if __name__ == '__main__':
    for arg in sys.argv:
        if '-u=' in arg:
            user = arg.split('=')[-1]
        elif '-p=' in arg:
            password = arg.split('=')[-1]
        elif '-s=' in arg:
            send_to = arg.split('=')[-1]

    subject = '[Resultados - ELO Clubes]'
    body = 'Seguem resultados.'
    attachments = glob('*.txt')
    enviado = False
    while not enviado:
        try:
            send(user, password, send_to, subject, body, attachments)
            enviado = True
        except:
            pass