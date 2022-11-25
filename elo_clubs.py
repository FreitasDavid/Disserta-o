import os

import json
import numpy as np
import pandas as pd
from glob import glob
from copy import copy, deepcopy
from itertools import product

'''
Algoritmo ELO clubes
'''

class elo_clubes:
    def __init__(self, jogos, forcas, Ki = 40, Kn = 25, filtro = 0, Hi = 120, M = 0.2, atualizar_H = False, divisoes = None):
        if divisoes != None:
            if type(Kn) == list:
                pass
            else:
                Kn = [Kn for i in range(max(divisoes) + 1)]
            
            if type(Ki) == list:
                pass
            else:
                Ki = [Ki for i in range(max(divisoes) + 1)]
            
            if type(Hi) == list:
                pass
            else:
                Hi = [Hi for i in range(max(divisoes) + 1)]
                
        self.n_clubes = np.max(jogos) + 1
        self.jogos_base = jogos
        forcas = list(forcas)
        while len(forcas) < self.n_clubes:
            forcas.append(forcas[-1])
            
        self.forcas_iniciais = forcas
        self.Ki = Ki
        self.Kn = Kn
        self.filtro = filtro
        self.Hi = Hi
        self.M = M
        self.att_H = atualizar_H
        self.Hs = [self.Hi for i in range(self.n_clubes)]
        self.divisoes = divisoes
        
    def show_params(self):
        print(f'Ki = {self.Ki}')
        print(f'Kn = {self.Kn}')
        print(f'filtro = {self.filtro}')
        print(f'Hi = {self.Hi}')
        print(f'M = {self.M}')
        print(f'Atualizar parâmetro de mando de campo: {self.att_H}')

    def score_esperado(self, RA, RB, H):
        return (1 + (10 ** ((RB - (H + RA)) / 400))) ** (-1)

    def atualiza_rating(self, RA, RB, SA, SB, KA, KB, H):
        EA = self.score_esperado(RA, RB, H)
        EB = 1 - EA
        CA = (SA - EA) * KA
        CB = (SB - EB) * KB
        RA = RA + CA
        RB = RB + CB
        if self.att_H:
            H = H + CA

        return RA, RB, H

    def ELO(self):
        forcas = self.forcas_iniciais.copy()
        n_jogos = len(self.jogos_base)
        jogados = [0 for i in range(self.n_clubes)]
        for i in range(n_jogos):
            cA, sA, sB, cB = self.jogos_base[i, :]
            Da = sA - sB
            if sA > sB:
                SA = 1 + (abs(Da) - 1) * self.M
            elif sA == sB:
                SA = 0.5
            else:
                SA = 0 - (abs(Da)  - 1) * self.M

            SB = 1 - SA
            
            if self.divisoes == None:
                if jogados[cA] < self.filtro:
                    KA = self.Ki
                else:
                    KA = self.Kn

                if jogados[cB] < self.filtro:
                    KB = self.Ki
                else:
                    KB = self.Kn
                    
                H = self.Hs[cA]
            else:
                if jogados[cA] < self.filtro:
                    KA = self.Ki[self.divisoes[i]]
                else:
                    KA = self.Kn[self.divisoes[i]]

                if jogados[cB] < self.filtro:
                    KB = self.Ki[self.divisoes[i]]
                else:
                    KB = self.Kn[self.divisoes[i]]
                    
                H = self.Hs[cA][self.divisoes[i]]
                
            RA, RB = forcas[cA], forcas[cB]
            RA, RB, H = self.atualiza_rating(RA, RB, SA, SB, KA, KB, H)
            forcas[cA], forcas[cB] = RA, RB
            if self.divisoes == None:
                self.Hs[cA] = H
            else:
                self.Hs[cA][self.divisoes[i]] = H

        return forcas

def treat_club(club):
    club = club.replace('Saf ', '')
    club = club.replace('S.a.f ', '')
    club = club.replace('S.A.F ', '')
    club = club.replace('Fc ', '')
    club = club.replace('FC ', '')
    club = club.replace('Futebol Clube ', '')
    club = club.replace('FUTEBOL CLUBE ', '')
    club = club.replace('F. C. ', '')
    club = club.replace('A.c. ', '')
    club = club.replace('Ltda ', '')
    club = club.replace('Associacao Desportiva ', '')
    club = club.replace('Esporte Clube ', '')
    club = club.replace('Sociedade Esportiva ', '')
    club = club.replace('-ap', '')
    club = club.replace('Sport Club ', '')
    club = club.replace('- Vn ', '')
    club = club.replace('- VN ', '')
    club = club.replace('Atletico', 'Atlético')
    club = club.replace('Vitoria', 'Vitória')
    club = club.replace('A.b.c. / RN', 'ABC / RN')
    club = club.replace('Abc / RN', 'ABC / RN')
    club = club.replace('AVAÍ / SC', 'Avaí / SC')
    club = club.replace('A.s.a. / AL', 'ASA / AL')
    club = club.replace('America / MG', 'América / MG')
    club = club.replace('América de Natal / RN', 'América / RN')
    club = club.replace('AMÉRICA / RN', 'América / RN')
    club = club.replace('Atlético / PR', 'Athletico Paranaense / PR')
    club = club.replace('ATLETICO / PR', 'Athletico Paranaense / PR')
    club = club.replace('Atlético / PR', 'Athletico Paranaense / PR')
    club = club.replace('Sobradinho (df) / DF', 'Sobradinho / DF')
    club = club.replace('ÁGUIA NEGRA / MS', 'Águia Negra / MS')
    club = club.replace('Aguia Negra / MS', 'Águia Negra / MS')
    club = club.replace('Aguia / PA', 'Águia de Marabá / PA')
    club = club.replace('Ypiranga Rs / RS', 'Ypiranga / RS')
    club = club.replace('Villa Nova A.c. / MG', 'Villa Nova / MG')
    club = club.replace('Veranopolis / RS', 'Veranópolis / RS')
    club = club.replace('União / MT', 'União de Rondonópolis / MT')
    club = club.replace('Ser Caxias / RS', 'Caxias / RS')
    club = club.replace('Sampaio Correa / MA', 'Sampaio Corrêa / MA')
    club = club.replace('SAMPAIO CORREA / MA', 'Sampaio Corrêa / MA')
    club = club.replace('SANTOS / SP', 'Santos / SP')
    club = club.replace('Bragantino / SP', 'Red Bull Bragantino / SP')
    club = club.replace('MURICI / AL', 'Murici / AL')
    club = club.replace('River / PI', 'Ríver / PI')
    club = club.replace('River A.c. / PI', 'Ríver / PI')
    club = club.replace('RÍVER / PI', 'Ríver / PI')
    club = club.replace('REAL NOROESTE / ES', 'Real Noroeste / ES')
    club = club.replace('Real Noroeste Capixaba / ES', 'Real Noroeste / ES')
    club = club.replace('PONTE PRETA / SP', 'Ponte Preta / SP')
    club = club.replace('PIAUÍ / PI', 'Piauí / PI')
    club = club.replace('Operario / PR', 'Operário / PR')
    club = club.replace('Luziania / DF', 'Luziânia / DF')
    club = club.replace('INDEPENDENTE / PA', 'Independente / PA')
    club = club.replace('Independente Tucuruí / PA', 'Independente / PA')
    club = club.replace('Guarany de Sobral / CE', 'Guarany / CE')
    club = club.replace('Guarani de Juazeiro / CE', 'Guarani / CE')
    club = club.replace('Crb / AL', 'CRB / AL')
    club = club.replace('Criciuma / SC', 'Criciúma / SC')
    club = club.replace('Csa / AL', 'CSA / AL')
    club = club.replace('FIGUEIRENSE / SC', 'Figueirense / SC')
    club = club.replace('FORTALEZA / CE', 'Fortaleza / CE')
    club = club.replace('C. R. B. / AL', 'CRB / AL')
    club = club.replace('C.r.a.c. / GO', 'CRAC / GO')
    club = club.replace('C.r.b. / AL', 'CRB / AL')
    club = club.replace('C.s.a. / AL', 'CSA / AL')
    club = club.replace('CAXIAS / RS', 'Caxias / RS')
    club = club.replace('CORITIBA / PR', 'Coritiba / PR')
    club = club.replace('CRICIÚMA / SC', 'Criciúma / SC')
    club = club.replace('Atlético Cearense / CE', 'Atlético / CE')
    club = club.replace('Atlético Roraima / RR', 'Atlético / RR')
    club = club.replace('BOTAFOGO / PB', 'Botafogo / PB')
    club = club.replace('BOTAFOGO / RJ', 'Botafogo / RJ')
    club = club.replace('Asa / AL', 'ASA / AL')
    club = club.replace('A.s.s.u. / RN', 'ASSU / RN')
    club = club.replace('Xv de Piracicaba / SP', 'XV de Piracicaba / SP')
    club = club.replace('Urt / MG', 'URT / MG')
    club = club.replace('Arapongas Esporte Clube / PR', 'Arapongas / PR')
    club = club.replace('Jacobina Ec / BA', 'Jacobina / BA')
    club = club.replace('Ge Juventus / SC', 'Juventus / SC')
    club = club.replace('TREZE / PB', 'Treze / PB')
    club = club.replace('S.francisco / PA', 'S. Francisco / PA')
    club = club.replace('Pstc / PR', 'PSTC / PR')
    club = club.replace('Prospera / SC', 'Próspera / SC')
    club = club.replace('Marilia / SP', 'Marília / SP')
    club = club.replace('Macae / RJ', 'Macaé / RJ')
    club = club.replace('Macapa / AP', 'Macapá / AP')
    club = club.replace('G.a.s / RR', 'G.A.S. / RR')
    club = club.replace('Cse / AL', 'CSE / AL')
    club = club.replace('Ca Patrocinense / MG', 'Atlético Patrocinense / MG')
    
    return club

