#include <iostream>

int main(int argc, char const *argv[])
{
	int test[1000][1000];
	int test2[1000][1000];
	int *a = new(int[100000]);
	for(int i(0); i<1000; ++i) {
		for(int j(0); j<1000; ++j){
			test[i][j]= 1;
			test2[i][j] = test[i][j];
		}
	}
	std::cout<<"hola\n";
	return 0;
}