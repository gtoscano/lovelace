#include <stdio.h>
#include <stdlib.h>

int main (int argc, char const *argv[])
{
	size_t i, n , x, suma=0; //se usa size_t en la suma para cumplir con las restricciones

	scanf("%zu", &n); //lees por teclado la cantidad de n numeros 
		             //que leeras a partir de aqui, y que tendras que sumar
		
	for(i = 0; i < n; ++i){
		scanf("%zu", &x);
		suma += x;
	}
	printf("%zu\n",suma); //ojo, se imprimi'o el n'umero sin espacio en blanco,
 						 // y posteriormente se le dio un 'unico retorno de l'inea
	return 0;
}
