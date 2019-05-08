###############################################################################
#Nome: Mateus Agostinho dos Anjos											  #
#NUSP: 9298191																  #
#EP3                                                                          #
#Python3                                                                      #
###############################################################################
import sys
import queue

#Funcao para imprimir os Vertices do Grafo
def imprimeVertices(fragmentos):
	print("Vertices:", end='\n\n')
	for i in range (len(fragmentos)):
		print(i, fragmentos[i], end='\n\n')
	return	
#Funcao que cria a Matriz utilizada para calcular as
#sobreposicoes
def criaMatriz(fragmentos):
	matriz = [0] * len(fragmentos)
	for i in range (len(fragmentos)):
		matriz[i] = [0] * len(fragmentos)	
	return matriz
#funcao que cria matriz de sobreposicoes
#posicao (i, j) da matriz contem a sobreposicao
#de prefixos de i com sufixos de j
def calculaSobreposicao(matriz, fragmentos):
	for i in range (len(fragmentos)):
		for j in range(len(fragmentos)):
			if (i != j):
				l = 1
				k = len(fragmentos[j]) - 1
				sobrepos = 0
				while (l <= len(fragmentos[i]) and k >= 0):
					if (fragmentos[i][:l] == fragmentos[j][k:]):
						sobrepos = l
					l = l + 1
					k = k - 1
				matriz[i][j] = sobrepos
			else:
				matriz[i][j] = 0		
	return		
#Funcao que retira as sobreposicoes (arestas) que sao
#menores que o parametro t passado na linha de comando,
#criando um grafo cujos vertices sao os fragmentos e as
#arestas sao as sobreposicoes, maiores ou iguais a  t, 
#entre os fragmentos.
def retiraArestas(matriz, fragmentos, t):
	grafo = {}
	for i in range (len(fragmentos)):
		for j in range(len(fragmentos)):
			if (matriz[i][j] >= t):
				grafo[(j, i)] = matriz[i][j]		
	return grafo	
#Funcao que imprime as arestas do grafo conforme pedido no enunciado
def imprimeArestas(grafo):
	print("Arestas:", end='\n\n')
	for vertice in sorted(grafo):
		print(vertice[0], "->", vertice[1], "^", grafo[vertice], end='\n\n')
	return
#Funcao que devolve uma ordenacao topologica do grafo passado, porem
#com as especificacoes do enunciado essa ordenacao sera um passeio
#hamiltoniano do grafo.
def passeioHamiltoniano(grafo, k):
	auxGrafo = grafo.copy()
	#lista que guarda o passeio hamiltoniado
	passeio = []
	#fila de vertices que nao possuem arestas de entrada
	semEntrada = queue.Queue()
	#Lista que guarda arestas que chegam num determinado vertice
	#entradas[i] guarda todos os vertices que sai uma aresta e que chega em i
	entradas = [0] * k
	#Lista que guarda as arestas que saem de um determinado vertice
	#saidas[i] guarda todos os vertices que recebem uma aresta que sai de i
	saidas = [0] * k
	for i in range (k):
		entradas[i] = []
		saidas[i] = []
	#preenche a lista de entradas e saidas
	for i in range (k):
		for j in range (k):
			if ((j, i) in auxGrafo):
				entradas[i].append(j)
				saidas[j].append(i)
	#preenche a fila de vertices sem entrada			
	for i in range (k):
		if (len(entradas[i]) == 0):
			semEntrada.put(i)		
	#Obtem uma ordem topologica do grafo, nas descricoes do EP
	#esta ordem topologica sera um passeio hamiltoniano
	while (not semEntrada.empty()):
		n = semEntrada.get()
		passeio.append(n)
		for m in saidas[n]:
			if ((n, m) in auxGrafo):
				auxGrafo.pop((n, m), None)
				entradas[m].remove(n)
				if (len(entradas[m]) == 0):
					semEntrada.put(m)								
	return passeio
#Funcao de impressao da supersequencia e das sobreposicoes dos
#fragmentos.
def imprimeSuperseqeLayout(passeio, fragmentos, grafo):
	
	print("Supersequencia comum e Layout dos fragmentos:", end = '\n\n')

	superSeq = []
	#lista das sobreposicoes entre fragmentos adjacetes no passeio
	#obtido.
	sobrepos = [0] * len(fragmentos)
	for i in range (len(passeio) - 1):
		sobrepos[i] = grafo[(passeio[i], passeio[i+1])]

	#monta a supersequencia a partir dos fragmentos
	k = 0
	for i in passeio:
		for j in range (len(fragmentos[i]) - sobrepos[k]):
			superSeq.append(fragmentos[i][j])	
		k = k + 1
	#imprime a supersequencia	
	for i in range (len(superSeq)):
		print(superSeq[i], end = '')
	print(end = '\n\n')
	
	#impressao da tabela de sobreposicoes
	offset = 0
	totalCarac = len(superSeq)
	numCarac = 0
	k = 0
	for i in passeio:
		#imprime os "-" iniciais
		for j in range (offset):
			print("-", end = '')
		#imprime o fragmento i	
		print(fragmentos[i], end = '')
		#variaveis para localizar onde o proximo fragmento
		#devera ser impresso (offset) e quantos caracteres foram
		#impressos nessa iteracao (numCarac)
		numCarac = offset + len(fragmentos[i])
		offset = numCarac - sobrepos[k]
		k = k + 1
		#imprime os "-" restantes
		for j in range (totalCarac - numCarac):
			print("-", end = '')
		print("", i)
		print()
	#imprime a supersequencia apos a tabela (como pede o enunciado)		
	for i in range (len(superSeq)):
		print(superSeq[i], end = '')
	print(end = '\n\n')
	return

def main():
	print()
	#obtencao dos parametros da linha de comando
	fragmentos = []
	t = int(sys.argv[1])
	for i in range (2, len(sys.argv)):
		fragmentos.append(sys.argv[i])
	#execucao do codigo que resolve o problema, seguindo as instrucoes
	#do enunciado	
	imprimeVertices(fragmentos)	
	matriz = criaMatriz(fragmentos)
	calculaSobreposicao(matriz, fragmentos)
	grafo = retiraArestas(matriz, fragmentos, t)
	imprimeArestas(grafo)
	passeio = passeioHamiltoniano(grafo, len(fragmentos))
	imprimeSuperseqeLayout(passeio, fragmentos, grafo)
main()