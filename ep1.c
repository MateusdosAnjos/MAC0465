/*Mateus Agostinho dos Anjos
//NUSP: 9298191
//Compilado com:  gcc -Wall -ansi -pedantic -O2 -o ep1 ep1.c 
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

/*constantes utilizadas
*/
#define gap -2
#define mismatch -1
#define match 1
#define SPACE '-'

/*variaveis globais
*/
char *alignS;
char *alignT;
char *revS;
char *revT;

/*funcao que calcula o maximo entre a, b, c
*/
int max(int a, int b, int c) {
	if (a >= b && a >= c) return a;
	else if (b >= c) return b;
	else return c;
}

/*funcao que faz avaliacao de s[i] e t[j]
*/
int p(int i, int j, char *s, char *t) {
	if (s[i] == t[j]) return match;
	else return mismatch;
}

/*funcao que calcula a melhor pontuacao para um alinhamento
//local entre s[1...i] e t[1...j]. Os indices i, j sao
//armazenados em *x e *y
*/
void melhorPontuacao(char *s, char *t, int *x, int *y) {
	int *a;
	int i, j, m, n, anterior, temp, pontuacaoMax, iMax = 0, jMax = 0;
	
	m = (int) (strlen(s));
	n = (int) (strlen(t));

	pontuacaoMax = (m+n) * (-2);

	a = malloc (n * (int)sizeof(int));

	for (j = 0; j <= n; j++) {
		a[j] = j * gap;
	}
	for (i = 1; i <= m; i++) {
		anterior = a[0];
		a[0] = i * gap;
		for (j = 1; j <= n; j++) {
			temp = a[j];
			a[j] = max((a[j] + gap), (anterior + p(i-1, j-1, s, t)), (a[j-1] + gap));
			if (a[j] >= pontuacaoMax) {
				iMax = i;
				jMax = j;
				pontuacaoMax = a[j];
			}
			anterior = temp;
		}
	}
	/*o indice inicial deste programa eh 0, enquanto o
	//indice dos algoritmos do livro comecam de 1
	*/	
	*x = iMax - 1;
	*y = jMax - 1;
	return;
}

/*funcao retirada do livro que calcula o bestScore do alinhamento
//entre s[a..b] e t[c..d]
*/
void bestScore(char *s, int a, int b, char *t, int c, int d, int *fixSim) {
	int i, j, m, n, anterior, temp;
	
	m = b - a;
	n = d - c;

	for (j = 0; j <= n; j++) {
		fixSim[j] = j * gap;
	}
	for (i = 1; i <= m; i++) {
		anterior = fixSim[0];
		fixSim[0] = i * gap;
		for (j = 1; j <= n; j++) {
			temp = fixSim[j];
			fixSim[j] = max((fixSim[j] + gap), (anterior + p(i-1, j-1, s, t)), (fixSim[j-1] + gap));
			anterior = temp;
		}
	}	
	return;
}

/*funcao que inverte uma string x
*/
char *inverte(char *x) {
	char *inv;
	int i, j = 0;
	inv = malloc (strlen(x) * sizeof(char));
	for (i = (strlen(x) - 1); i >= 0; i--) {
		inv[j] = x[i];
		j++;
	}
	return inv;
}

/*Algoritmo 3.6 do livro (Setubal)
//queremos alinhar s[a..b] com t[c..d] sendo a, b, c, d
//inteiros encontrados previamente utilizando os alinhamentos
//locais
*/
int align(char *s, char *t, int a, int b, int c, int d, int start, int end) {
	int posMax, vMax, i, j, middle;
	int *prefSim, *suffSim;
	char typeMax;

	prefSim =  malloc ((b-a) * (int)sizeof(int));
	suffSim =  malloc ((d-c) * (int)sizeof(int));

	/*se alguma sequencia for vazia, alinhamos o remanescente com gap
	*/
	if ((b - a) <= 0 || (d - c) <= 0) {
		end = start + max((b - a), (d - c), -10000);
	}
	else {
		/*pegamos aproximadamente o meio da sequencia
		*/
		i = floor((a + b)/2);
		/*Pagina 60 do livro diz:
		//BestScore(s[a..i-1], t[c..d], prefSim) returns in prefSim the
		//similarities between s[a..i-1] and t[c..j] for all j in c-1..d.
		*/
		bestScore(s, a, i-1, t, c, d, prefSim);
		/*Pagina 60 do livro diz:
		//BestScoreRev(s[i+1..b], t[c..d], suffSim) returns in suffSim the
		//similarities between s[i+1..b] and t[j+1..d] for all j in c-1..d
		//veja que para c-1 -> j+1 = (c-1) + 1 -> j+1 = c
		*/
		bestScore(s, i+1, b, t, c, d, suffSim);/*BestScoreRev*/
		/*Seguindo o que esta no pseudoCodigo do livro temos:
		*/
		posMax = c - 1;
		typeMax = SPACE;
		vMax = prefSim[c-1] + gap + suffSim[c-1];
		for (j = c; j <= d; j++) {
			if (prefSim[j-1] + p(i, j, s, t) + suffSim[j] > vMax) {
				posMax = j;
				typeMax = s[i];
				vMax = prefSim[j-1] + p(i, j, s, t) + suffSim[j];
			}
			if (prefSim[j] + gap + suffSim[j] > vMax) {
				posMax = j;
				typeMax = SPACE;
				vMax = prefSim[j] + gap + suffSim[j];
			}
		}
		middle = (a+(i-1))/2;
		if (typeMax == SPACE) {
			end = align(s, t, a, i - 1, c, posMax, start, middle);
			alignS[middle] = s[i];
			alignT[middle] = SPACE;
			end = align(s, t, i + 1, b, posMax + 1, d, middle + 1, end);	
		}
		else { /*typeMax == SYMBOL*/
			end = align(s, t, a, i - 1, c, posMax - 1, start, middle);
			alignS[middle] = s[i];
			alignT[middle] = t[posMax]; 
			end = align(s, t, i + 1, b, posMax + 1, d, middle + 1, end);
		}
	}
	return end;
}

/*funcao que imprime o alinhamento encontrado
*/
void imprimeAlinhamento(int n) {
	int i;

	printf("Alinhamento:\n");
	for (i = 0; i < n; i++) {
		if (alignS[i] != 0)
			printf("%c", alignS[i]);
		else {
			printf("-");
		}
	}
	printf("\n");
	for (i = 0; i < n; i++) {
		if (alignT[i] != 0)
			printf("%c", alignT[i]);
		else {
			printf("-");
		}
	}
	printf("\n");
	return;  
}

int main(int argv, char **argc) {
	char *s, *t;
	int a, b, c, d, n;

	/*as duas sequencias a serem alinhadas
	*/
	s = "ACTG";
	t = "GCTC";

	n = max(strlen(s), strlen(t), 0);

	/*Global*/
	alignS = malloc (n * sizeof(char));
	alignT = malloc (n * sizeof(char));
	revS = malloc (strlen(s) * sizeof(char));
	revT = malloc (strlen(t) * sizeof(char));
	revS = inverte(s);
	revT = inverte(t);
	
	melhorPontuacao(s, t, &b, &d);

	melhorPontuacao(revS, revT, &a, &c);

	/*meus indices comecam do 0, enquanto o
	//algoritmo do livro indexa o inicio de 1
	//por isso algumas operacoes desse tipo
	*/
	a = ((strlen(s) - 1) - a);
	c = ((strlen(t) - 1) - c);

	printf("s = %s\n", s);
	printf("t = %s\n", t);
	
	/*O alinhamento deve ser feito para s[a...b] e t[c...d]
	*/
	n = align(s, t, a, b, c, d, 1, max((b-a), (d-c), 0));
	
	imprimeAlinhamento(n);
	/*liberando memoria*/
	free(alignS);
	free(alignT);
	return 0;
}