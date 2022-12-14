from elo_clubs import *
import sys
import os

if __name__ == '__main__':
    os.chdir('Arquivos')
    M, dim = sys.argv[-2], sys.argv[-1]
    M = float(M.split('=')[-1])
    dim = int(dim.split('=')[-1])
    div_considerada = sys.argv[-3].split('=')[-1]

    ranking = pd.read_excel('Ranking times brasileiros.xlsx')
    ranking['Clube'] = ranking['Clube'].apply(treat_club)
    clubes = ranking['Clube'].values.tolist()
    clubes = {clubes[i].strip() : i for i in range(len(clubes))}

    # separando as partidas de treino
    jogos = []
    for ano in range(2013, 2022):
        jogos.append(f'Serie_A-{ano}-games.json')
        jogos.append(f'Serie_B-{ano}-games.json')
        jogos.append(f'Serie_C-{ano}-games.json')
        jogos.append(f'Serie_D-{ano}-games.json')

    n_jogos_treino = 0
    for jogo in jogos:
        with open(jogo, 'r') as f:
            games = json.load(f)

        n_jogos_treino += len(games)

    partidas_treino = np.zeros((n_jogos_treino, 4), dtype = int)
    linha = 0
    divisoes_treino = []
    for jogo in jogos:
        divisao = jogo[:7]
        with open(jogo, 'r') as f:
            games = json.load(f)

        for game in games:
            divisoes_treino.append(ord(divisao[-1]) - 65)
            mandante = games[game]['Mandante']
            visitante = games[game]['Visitante']
            resultado = games[game]['Resultado']
            resultado_m, resultado_v = resultado.upper().split(' X ')
            resultado_m = int(resultado_m)
            resultado_v = int(resultado_v)
            if mandante not in clubes:
                clubes[mandante] = len(clubes) +1
                add = {'POS' : [len(ranking) + 1],
                       'Clube' : [mandante],
                       'Estado' : [mandante[-2:]],
                       'Pontos dim. 2' : [1078],
                       'Pontos dim. 3' : [865],
                       'Pontos dim. 4' : [656],
                       'Pontos dim. 5' : [445],
                       'Pontos dim. 10' : [390],
                       'Repetido' : ['SIM']}

                ranking = pd.concat([ranking, pd.DataFrame(add)], ignore_index = True)

            mandante = clubes[mandante]
            if visitante not in clubes:
                clubes[visitante] = len(clubes) + 1
                add = {'POS' : [len(ranking) + 1],
                       'Clube' : [visitante],
                       'Estado' : [visitante[-2:]],
                       'Pontos dim. 2' : [1078],
                       'Pontos dim. 3' : [865],
                       'Pontos dim. 4' : [656],
                       'Pontos dim. 5' : [445],
                       'Pontos dim. 10' : [390],
                       'Repetido' : ['SIM']}

                ranking = pd.concat([ranking, pd.DataFrame(add)], ignore_index = True)

            visitante = clubes[visitante]
            partidas_treino[linha, :] = [mandante, resultado_m, resultado_v, visitante]
            linha += 1

    # separando as partidas de teste
    jogos = []
    ano = 2022
    jogos.append(f'Serie_A-{ano}-games.json')
    jogos.append(f'Serie_B-{ano}-games.json')
    jogos.append(f'Serie_C-{ano}-games.json')
    jogos.append(f'Serie_D-{ano}-games.json')

    n_jogos_teste = 0
    for jogo in jogos:
        with open(jogo, 'r') as f:
            games = json.load(f)

        n_jogos_teste += len(games)

    partidas_teste = np.zeros((n_jogos_teste, 4), dtype = int)
    linha = 0
    divisoes_teste = []
    for jogo in jogos:
        divisao = jogo[:7]
        with open(jogo, 'r') as f:
            games = json.load(f)

        for game in games:
            divisoes_teste.append(ord(divisao[-1]) - 65)
            mandante = games[game]['Mandante']
            visitante = games[game]['Visitante']
            resultado = games[game]['Resultado']
            resultado_m, resultado_v = resultado.upper().split(' X ')
            resultado_m = int(resultado_m)
            resultado_v = int(resultado_v)
            if mandante not in clubes:
                clubes[mandante] = len(clubes) + 1

            mandante = clubes[mandante]
            if visitante not in clubes:
                clubes[visitante] = len(clubes) + 1

            visitante = clubes[visitante]
            partidas_teste[linha, :] = [mandante, resultado_m, resultado_v, visitante]
            linha += 1

    base_dimensoes = {2 : 1078, 3 : 865, 4 : 656, 5 : 445, 10 : 390}
    params = []
    resultados = []
    resultados_totais = []
    ratings_pos_treino = []
    for M, K_A, K_B, K_C, K_D, Hi_A, Hi_B, Hi_C, Hi_D, dim in product([M], #np.array([*range(4, 5)]) / 10, # M
                                                                      [2, 5, 8, 10], # K_A
                                                                      [9, 12, 15, 18], # K_B
                                                                      [10, 13, 16, 20], # K_C
                                                                      [13, 16, 19, 22], # K_D
                                                                      [100, 150, 200, 250], # Hi_A
                                                                      [150, 200, 250, 300], # Hi_B
                                                                      [200, 250, 300, 350], # Hi_C
                                                                      [200, 250, 300, 350], # Hi_D
                                                                      [dim]): # dim

        Kn = [K_A, K_B, K_C, K_D]
        Hi = [Hi_A, Hi_B, Hi_C, Hi_D]
        params.append([M, Kn.copy(), Hi.copy(), dim])

        # definindo o modelo
        forcas = list(copy(ranking[f'Pontos dim. {dim}'].values.astype('float64')))
        n_clubes = max(np.max(partidas_treino), np.max(partidas_teste)) + 1
        while len(forcas) < n_clubes:
            forcas.append(base_dimensoes[dim])

        modelo = elo_clubes(partidas_treino,
                            forcas,
                            Hi = Hi,
                            Kn = Kn,
                            M = M,
                            divisoes = divisoes_treino)

        # treina o modelo (faz a evolu????o do elo com os jogos at?? 2021)
        ratings = modelo.ELO()
        ratings_pos_treino.append(deepcopy(ratings))

        # testa (simula os jogos de 2022)
        acertos = 0
        total = 0
        for i, partida in enumerate(partidas_teste):
            # coleta os dados da partida
            mandante, sA, sB, visitante = partida

            # resultado final
            if sA > sB:
                resultado_partida = 1
            elif sA == sB:
                resultado_partida = 0.5
            else:
                resultado_partida = 0

            # pega os ratings
            if len(ratings) > mandante:
                RA = ratings[mandante]
            else:
                RA = base_dimensoes[dim]

            if len(ratings) > visitante:
                RB = ratings[visitante]
            else:
                RB = base_dimensoes[dim]

            # resultado esperado
            p = modelo.score_esperado(RA, RB, Hi[divisoes_teste[i]])
            if p > 2/3:
                resultado_previsto = 1
            elif p < 1/3:
                resultado_previsto = 0
            else:
                resultado_previsto = 0.5

            # computa acertos
            if resultado_previsto == resultado_partida:
                acertos += divisoes_teste[i] == ord(div_considerada) - 65

            total += divisoes_teste[i] == ord(div_considerada) - 65

            # atualiza ranking
            Da = sA - sB
            if sA > sB:
                SA = 1 + (abs(Da) - 1) * modelo.M
            elif sA == sB:
                SA = 0.5
            else:
                SA = 0 - (abs(Da)  - 1) * modelo.M

            SB = 1 - SA
            while len(modelo.Hs) < mandante + 1:
                modelo.Hs += [modelo.Hi]

            H = modelo.Hs[mandante][divisoes_teste[i]]
            RA, RB, H = modelo.atualiza_rating(RA, RB, SA, SB,
                                               modelo.Kn[divisoes_teste[i]], modelo.Kn[divisoes_teste[i]], H)
            ratings[mandante], ratings[visitante] = RA, RB
            modelo.Hs[mandante][divisoes_teste[i]] = H

        resultado = acertos / total
        resultados.append(resultado)
        resultados_totais.append([acertos, total])

        os.chdir('..')
        print(resultado, [acertos, total], [M, Kn.copy(), Hi.copy(), dim])
