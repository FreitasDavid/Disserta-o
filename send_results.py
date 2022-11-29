from glob import glob

import sys
from mail_delivery import *
from time import sleep

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
    tentativas = 0
    while not enviado or tentativas < 10:
        try:
            send(user, password, send_to, subject, body, attachments)
            enviado = True
        except:
            tentativas += 1
            sleep(5)