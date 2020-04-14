#include <string.h>
#include <stdio.h>

void wrong(){
	printf("Access Failed !??? \n");
}

void correct(){
	printf("Access Granted !! \n");
}

int main(int argc, char *argv[]){
        if(argc==2) {
        	int key = 0;
			printf("Checking License: %s\n", argv[1]);
			if(strcmp(argv[1], "Nyaaa")==0) {
				if(key == 0){
					wrong();
				}
				else{
					correct();
				}
			}
			else {
				printf("WRONG Again!\n");
			}
		} 
		else {
			printf("Usage: <key>\n");
		}
		return 0;
	}