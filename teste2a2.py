def main():
	matriz = ['1', '2', '3', '4', '5']
	for i in range (len(matriz) - 1):
		for j in range (i+1, len(matriz)):
			print("( " + matriz[i] + matriz[j] + " )", end=' ')
		print()
main()			