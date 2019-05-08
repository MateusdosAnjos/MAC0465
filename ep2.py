#Mateus Agostinho dos Anjos
#NUSP 9298191
#python3

import sys
import math

#Valores de match, mismatch e gap serao lidos
#da linha de comando, estes sao apenas os valores
#padrao iniciais
match = 1
mismatch = -1
gap = -2
menosinfinito = float("-inf")
memoVal = {}

########################################################
###                 FUNCOES DE SCORE                 ###
########################################################
#trivial
def p(x, y):
	if (x == y): return match
	else: return mismatch

#funcao que calcula o score das k letras
#colocadas na lista bases.
def SPscore(bases, k):
	score = 0
	for i in range (k):
		for j in range (i+1, k):
			if (bases[i] == '-' and bases[j] == '-'):
				pass #caso de alinhamento entre 2 gaps score recebe 0
			elif (bases[i] == '-' or bases[j] == '-'):
				score = score + gap		
			else:	
				score = score + p(bases[i], bases[j])
	return score		
########################################################
###                CONSTRUIR O DELTA                 ###
########################################################
#Devolve o piso do log de n na base 2
def floorLog(n):
	lg = 0
	while (math.floor(n/2) > 0):
		lg += 1
		n = math.floor(n/2)
	return lg	

#Devolve uma matriz com n-1 linhas e em cada linha
#da matriz temos o numero correspondente da linha 
#na representacao binaria. Com isso formamos nosso 
#Delta definido no enunciado
def constroiDelta(n):
	numDeDigitos = floorLog(n)
	comb = [0] * n
	for i in range (n):
		comb[i] = [0] * numDeDigitos
		j = i
		c = numDeDigitos - 1
		while (math.floor(j/2) > 0):
			comb[i][c] = j%2
			c = c - 1
			j = math.floor(j/2)	
		comb[i][c] = j%2
	return comb
########################################################
###              VERIFICACOES DE INDICES             ###
########################################################
#funcao que verifica se algum indice eh menor que zero
#(negativo)	
def indiceNeg(seqIndex, k):
	for i in range (k):
		if (seqIndex[i] < 0): return True
	return False
#funcao que verifica se algum indice eh maior que zero
#(positivo)	
def indicePos(seqIndex, k):
	for i in range (k):
		if (seqIndex[i] > 0): return True
	return False	
########################################################
###           AUXILIARES DE "ALINHAMULT"             ###
########################################################
#funcao que seleciona as bases a serem alinhadas
def selecionaBases(S, seqIndex, delta, k):
	bases = [''] * k
	for i in range (k):
		if (delta[i] == 1):
			bases[i] = S[i][seqIndex[i]]
		else:
			bases[i] = '-'
	return bases			

#funcao que recebe duas listas x e y de mesmo tamanho k
#e para cada posicao i faz x[i] - y[i]
def subtracaoDeLista(x, y, k):
	aux = [0] * k
	for i in range (k):
		aux[i] = x[i] - y[i]
	return aux
########################################################
###     CALCULO DO SCORE DE ALINHAMENTO OTIMO        ###
########################################################
#funcao que calcula o alinhamento multiplo otimo recursivamente
def alinhaMult(S, seqIndex, delta, k):
    global memoVal
    score = menosinfinito
    #Caso em que o valor ja foi memorizado
    if (tuple(seqIndex) in memoVal): return memoVal[tuple(seqIndex)] 
    #Caso do indice negativo em alguma posicao
    if (indiceNeg(seqIndex, k)): return menosinfinito
    #Caso recursivo
    i = 0
    #iteramos para todas as combinacoes de nosso delta
    while (i < len(delta)):
    	bases = selecionaBases(S, seqIndex, delta[i], k)
    	score = max(score, (alinhaMult(S, subtracaoDeLista(seqIndex, delta[i], k), delta, k) + SPscore(bases, k)))
    	i = i + 1
    memoVal[tuple(seqIndex)] = score
    return score
########################################################
###         MOSTRA O ALINHAMENTO OTIMO               ###
########################################################
#funcao que recupera o alinhamento multiplo otimo
def recuperaAlinhamento(S, seqIndex, delta, k):
	alinhamento = [''] * k
	for i in range (k):
		alinhamento[i] = []
	score = memoVal[tuple(seqIndex)]
	while (indicePos(seqIndex, k)):
		for alinha in delta:
			posGeradora = subtracaoDeLista(seqIndex, alinha, k)
			bases = selecionaBases(S, seqIndex, alinha, k)
			if (tuple(posGeradora) in memoVal):
				if (score == (memoVal[tuple(posGeradora)] + SPscore(bases, k))):
					for i in range (k):
						alinhamento[i].append(bases[i])
					seqIndex = posGeradora
					score = memoVal[tuple(posGeradora)]
					break
	return alinhamento
#funcao que imprime o alinhamento no terminal da forma mais
#intuitiva
def imprimeAlinhamento(alinhamento, k):
	n = len(alinhamento[0])
	for i in range (k):
		j = n - 1
		while (j >= 0):
			print(alinhamento[i][j], end='')
			j = j - 1
		print()				
########################################################
###                      MAIN                        ###
########################################################
def main():
	global match, mismatch, gap
	#Atribui valores do enunciado
	match = int(sys.argv[1])
	mismatch = int(sys.argv[2])
	gap = int(sys.argv[3])
	k = int(sys.argv[4])
	#S eh uma lista das sequencias passadas
	S = []
	seqIndex = ['0'] * k
	#preenche S colocando 'X' na posicao 0 de cada
	#sequencia, pois o algoritmo indexa as sequencias 
	#de 1 a n
	for i in range (k):
		S.append(str(sys.argv[i+5]))
		S[i] = 'X' + S[i]
		#seqIndex guarda o index da ultima posicao
		#de cada sequencia
		seqIndex[i] = len(S[i]) - 1
	#calcula as combinacoes de 2^k - 1 alinhamentos	
	numComb = pow(2, k)	
	#delta eh o vetor de bits do enunciado
	delta = constroiDelta(numComb)
	#dicionario para memorizar os valores calculados
	memoVal[tuple(delta[0])] = 0
	#funcao que faz o calculo dos valores para o alinhamento
	#multiplo otimo	
	print("Max score: ",
		alinhaMult(S, seqIndex, delta[1:], k))
	alinhamento  = recuperaAlinhamento(S, seqIndex, delta[1:], k)
	imprimeAlinhamento(alinhamento, k)
main()