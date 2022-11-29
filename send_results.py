import sys
from mail_delivery import *
from time import sleep
from glob import glob

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