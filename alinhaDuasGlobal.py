import sys

gap = -2

#funcao que imprime uma matriz de m linhas
def imprime(matriz, m):
	for i in range (m):
		for j in range (len(matriz[i])):
			print(matriz[i][j], " ", end='')
		print()	
#trivial
def p(x, y):
	if (x == y): return 1
	else: return -1

#funcao que calcula o score das k letras
#colocadas na lista bases.
def SPscore(bases, k):
	score = 0
	for i in range (k):
		for j in range (i+1, k):
			if (bases[i] == '-' and bases[j] == '-'):
				pass #caso de alinhamento entre 2 gaps score recebe 0	
			else:	
				score = score + p(bases[i], bases[j])
	return score		

def align(s, t):
	m = len(s)
	n = len(t)
	a = [0] * n
	path = [''] * m
	for j in range (m):
		path[j] = [''] * n 
	for j in range (n):
		a[j] = j*gap
	for i in range (1, m):
		old = a[0]
		a[0] = i * gap
		for j in range (1, n):
			temp = a[j]
			a[j] = max(a[j] + gap, old + p(s[i], t[j]), a[j-1] + gap)
			if (temp + gap == a[j]): path[i][j] = 'left'
			elif ((old + p(s[i], t[j])) == a[j]): path[i][j] = 'diag'
			else: path[i][j] = 'up'
			old = temp
	for k in range (m):
		print(path[k])
	print()		
	k = m - 1
	l = n - 1
	index = max(m, n)
	alignS = [''] * index
	alignT = [''] * index
	while (k > 0 and l > 0):
		index = index - 1
		if (path[k][l] == 'diag'):
			alignS[index] = s[k]
			alignT[index] = t[l]
			k = k - 1
			l = l - 1
		elif (path[k][j] == 'up'):
			alignS[index] = '-'
			alignT[index] = t[l]
			l = l - 1
		else:
			alignS[index] = s[k]
			alignT[index] = '-'
			k = k - 1		
	print(alignS)
	print(alignT)						
def main():
	#Atribui valores do enunciado
	r = int(sys.argv[1])
	q = int(sys.argv[2])
	gap = int(sys.argv[3])
	k = int(sys.argv[4])
	#S eh uma lista das sequencias passadas
	S = []
	#M sera a matriz de valores a ser computados
	M = [0] * k
	#preenche S
	for i in range (k):
		S.append(str(sys.argv[i+5]))
	#inicializa M
	for i in range (k):
		M[i] = [0] * len(S[i])
	#imprime M	
	imprime(M, k)
	align(S[0], S[1])
	align(S[1], S[2])

main()