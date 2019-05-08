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
#                  Funcoes da p2                       #
########################################################
def montaColuna(alinhamento, i, k):
	coluna = [''] * k	
	for j in range (k):
		coluna[j] = alinhamento[j][i]
	return coluna

def contaFrequencia(coluna, k, frequencia):
	for i in range (k):	
		if (coluna[i] == '-'): frequencia[0] = frequencia[0] + 1
		if (coluna[i] == 'A'): frequencia[1] = frequencia[1] + 1
		if (coluna[i] == 'C'): frequencia[2] = frequencia[2] + 1
		if (coluna[i] == 'T'): frequencia[3] = frequencia[3] + 1
		if (coluna[i] == 'G'): frequencia[4] = frequencia[4] + 1
	
def zeraFrequencia(frequencia):
	for i in range (5):
		frequencia[i] = 0

def obtemConsenso(frequencia, k):
	for i in range (5):
		if (frequencia[i] > k/2):
			if (i == 0): return '-'
			if (i == 1): return 'A'
			if (i == 2): return 'C'
			if (i == 3): return 'T'
			if (i == 4): return 'G'
	return 'NDA'

def verificaBinaria(frequencia):
	simbDist = 0
	for i in range (5):
		if (frequencia[i] != 0): simbDist = simbDist + 1
	if (simbDist == 2): return True
	else: return False

def criaCaracteristica(coluna, consenso, k):
	carac = [0] * k
	for i in range (k):
		if (coluna[i] == consenso): carac[i] = 0
		else: carac[i] = 1
	return carac

def imprimeMatrizBin(matriz, k):
	print("Matriz de caracteristisas binarias:")
	for j in range (k):
		i = len(matriz) - 1
		while (i >= 0):
			print(matriz[i][j] ,end=' ')
			i = i - 1
		print()
def verificaCompat(matriz, k):
	#Primeiro ordenamos em ordem DECRESCENTE a matriz
	#de caracteristica
	matriz.sort(reverse=True)
	#Agora verificamos 2 a 2 as caracteristicas binarias (colunas)
	#devemos ter para todas as combinacoes:
	#uma esta contida na outra OU a interseccao das duas eh vazia
	#caso alguma dessas duas condicoes falhar, as caracteristicas sao
	#incompativeis
	intersec = 0
	#Pegamos todas as combinacoes 2 a 2
	for i in range (len(matriz)-1):
		for j in range (i+1, len(matriz)):
			#analisando se nao ha interseccao ou se um esta contido
			#no outro
			for l in range (k):
				#Ha interseccao
				if (matriz[i][l] == 1 and matriz[j][l] == 1):
					intersec = 1
				#Checando se ha interseccao, porem um nao esta contido
				#no outro	
				if (intersec and matriz[i][l] < matriz[j][l]):
					#portanto as caracteristicas sao incompativeis
					return False
			#zeramos interseccao e vamos para o proximo par 
			#(proxima iteracao)		
			intersec = 0
	return True	
						
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
	print()

##################################################################################
#                         Inicio do codigo referente a P2                        #
##################################################################################
	print("INICIO DA P2")
	#vetor frequencia [0] = '-', [1] = 'A' [2] = 'C' [3] = 'T' [4] = 'G'
	frequencia = [0] * 5
	matriz = []
	for i in range (len(alinhamento[0])):
		#monta a i-esima coluna de alinhamento
		coluna = montaColuna(alinhamento, i, k)
		#conta a frequencia das bases da iesima coluna
		contaFrequencia(coluna, k, frequencia)
		#Obtem o simbolo de consenso (NDA caso nao exista)
		consenso = obtemConsenso(frequencia, k)
		#Verifica se existe o consenso
		if (consenso != 'NDA'):
			#Verifica se a coluna eh binaria
			if (verificaBinaria(frequencia)):
				#criamos a caracteristica Binaria
				matriz.append(criaCaracteristica(coluna, consenso, k))
		#zera o vetor que conta as frequencias
		zeraFrequencia(frequencia)
	#Imprimindo a matriz de caracteristicas binarias
	imprimeMatrizBin(matriz, k)
	#Verifica Compatibilidade
	if(verificaCompat(matriz, k)):
		print("As caracteristicas sao compativeis.")
	else:
		print("As caracteristicas NAO sao compativeis.")

main()
