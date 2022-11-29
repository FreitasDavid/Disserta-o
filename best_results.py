import numpy as np
from glob import glob

if __name__ == '__main__':
    top = 10
    resultados = []
    params = []
    for result_file in glob('results_SA_*.txt'):
        with open(result_file, 'r') as f:
            results = f.readlines()
            
        for result in results:
            result = result.strip()
            porcentagem = result.split()[0]
            resultados.append(float(porcentagem))
            params.append(result)
            
    resultados = np.argsort(resultados)
    print('Série A:')
    for i in range(1, top + 1):
        print(params[resultados[-i]])
        
    print()
    resultados = []
    params = []
    for result_file in glob('results_SB_*.txt'):
        with open(result_file, 'r') as f:
            results = f.readlines()
            
        for result in results:
            result = result.strip()
            porcentagem = result.split()[0]
            resultados.append(float(porcentagem))
            params.append(result)
            
    resultados = np.argsort(resultados)
    print('Série A:')
    for i in range(1, top + 1):
        print(params[resultados[-i]])
        
    print()
    resultados = []
    params = []
    for result_file in glob('results_SC_*.txt'):
        with open(result_file, 'r') as f:
            results = f.readlines()
            
        for result in results:
            result = result.strip()
            porcentagem = result.split()[0]
            resultados.append(float(porcentagem))
            params.append(result)
            
    resultados = np.argsort(resultados)
    print('Série A:')
    for i in range(1, top + 1):
        print(params[resultados[-i]])
        
    print()
    resultados = []
    params = []
    for result_file in glob('results_SD_*.txt'):
        with open(result_file, 'r') as f:
            results = f.readlines()
            
        for result in results:
            result = result.strip()
            porcentagem = result.split()[0]
            resultados.append(float(porcentagem))
            params.append(result)
            
    resultados = np.argsort(resultados)
    print('Série A:')
    for i in range(1, top + 1):
        print(params[resultados[-i]])