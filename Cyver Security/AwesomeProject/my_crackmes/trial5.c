#include <string.h>
#include <stdio.h>

void correct1(){
	printf("Access Failed but be coloser 1 \n");
}

void correct2(){
	printf("Access Failed but be coloser 2 \n");
}

void correct3(){
	printf("Access Failed but be coloser 3 \n");
}

void correct4(){
	printf("Access Failed but be coloser 4 \n");
}

void correct5(){
	printf("Access Failed but be coloser 5 \n");
}

void correct6(){
	printf("Access Failed but be coloser 6 \n");
}

void correct7(){
	printf("Access Failed but be coloser , and maybe out of range \n");
}

void correct(){
	printf("Access Granted !! \n");
}

int main(int argc, char *argv[]){
			int key;
        	printf("Enter key from 1 -- 7 \n");
			scanf("%d", &key);
			if(key == 1) {
					correct1();
				}
			else if(key == 2){
					correct2();
				}
			else if(key == 3){
					correct3();
				}
			else if(key == 4){
					correct4();
				}
			else if(key == 5){
					correct5();
				}
			else if(key == 6){
					correct6();
				}
			else if(key == 7){
					correct7();
				}
			else{
					correct();
			}
		return 0;
	}