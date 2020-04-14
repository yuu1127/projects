#include <string.h>
#include <stdio.h>

int main(int argc, char *argv[]){
			char str1[20];
			printf("Enter password \n");
			scanf("%s", str1);
			
			if(strcmp(str1, "password")==0) {
				printf("Access Granted!\n");
			}
			else {
				printf("WRONG!\n");
			}
		return 0;
	}