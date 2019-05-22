#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>

// all the basic data structures and functions are included in this template
// you can add your own auxiliary functions as you like
// data structures representing DLList

// For time complexity :n == DLList->size

// data type for nodes
typedef struct DLListNode {
	int  value;  // value (int) of this list item
	struct DLListNode *prev;
	// pointer previous node in list
	struct DLListNode *next;
	// pointer to next node in list
} DLListNode;

//data type for doubly linked lists
typedef struct DLList{
	int  size;      // count of items in list
	DLListNode *first; // first node in list
	DLListNode *last;  // last node in list
} DLList;

// create a new DLListNode
DLListNode *newDLListNode(int it)
{
	DLListNode *new;
	new = malloc(sizeof(DLListNode));
	assert(new != NULL);
	new->value = it;
	new->prev = new->next = NULL;
	return new;
}

// create a new empty DLList
DLList *newDLList()
{
	DLList *L;

	L = malloc(sizeof (struct DLList));
	assert (L != NULL);
	L->size = 0;
	L->first = NULL;
	L->last = NULL;
	return L;
}

//if n = DLList->size O(n)
DLListNode  *joinDLL(DLListNode *head1,DLListNode *head2){
	//need to connect head and tail
  if(head1 == NULL){
    head1 = head2;
  }else{
    DLListNode *p = head1;
    while(p->next != NULL){	//roop p->size
			p = p->next;
		}
  p->next = head2;
	p->next->prev = p;
  }
  return head1;
}


// create a DLList from a text file
// put your time complexity analysis for CreateDLListFromFileDlist() here

//malloc() and free(), takes O(1) time.
//Then newList() O(1) O(n) + O(1) = O(n)
// O(n^2) + O(n) = O(n^2)
// Then Time Complexity is O(n^2)
DLList *CreateDLListFromFileDlist(const char *filename)
{
 // put your code here
	int num;
	char *stdin_name = "stdin";
	DLList *DL;
	DLListNode *all = NULL;
	char buffer[100];
	DL = newDLList();
	FILE *fp;

	if(strcmp(filename,stdin_name) == 0){
		fp = stdin;
		while(fgets(buffer, sizeof(buffer), fp)){	// roop the number of elements then Time complexity is O(n) = O(DLL->size)
			if (sscanf(buffer, "%d", &num) == 1){
				DLListNode *new = newDLListNode(num);		//O(1)
				all = joinDLL(all,new); // inside n roop , then O(n * n) = O(n^2)
				if(all->prev == NULL){
					DL->first = all;
				}
				DL->size++;
			}
			else{
				break;
			}
		}
		while(all != NULL){	//O(n)
			if(all->next == NULL){
				DL->last = all;
			}
			DLListNode *temp = all->next;
			all = temp;
		}
	}

	// if file open then time complexity is same as above
	else{
		if((fp = fopen(filename,"r"))==NULL){
			printf("file open failed\n");
			fclose(fp);
			exit(-1);
		}
	while(fscanf(fp, "%d",&num) != EOF){
	// while((num = getc(fp)) != EOF) {
		//printf("%d\n",num);
		// make new node
		DLListNode *new = newDLListNode(num);
		all = joinDLL(all,new);
		if(all->prev == NULL){
			DL->first = all;
		}
		DL->size++;
	}
	//Dl->last = new;
	while(all != NULL){
		if(all->next == NULL){
			DL->last = all;
		}
		DLListNode *temp = all->next;
		all = temp;
	}
	fclose(fp);
	}
	return(DL);
}


// clone a DLList
// put your time complexity analysis for cloneList() here

//O(n^2)
DLList *cloneList(DLList *u)
{
 // put your code here
 DLListNode *original = u->first;
 DLList *copyList = newDLList();
 copyList->size = u->size;
 DLListNode *all = NULL;
 //DLListNode *temp = newDLListNode(original->value);
 //copyList->first = temp;
 //DLListNode *copyNode = newDLListNode();
 //copyNode->value = u->first->value;
 //newList.first = u->first;
 while(original != NULL){			//O(n)
	 DLListNode *new = newDLListNode(original->value);
	 all = joinDLL(all,new);		//O(n)
	 if(all->prev == NULL){
		 copyList->first = all;
	 }
	 original = original->next;
 }

 while(all != NULL){
	 if(all->next == NULL){
		 copyList->last = all;
	 }
	 //DLListNode *temp = all->next;
	 //all = temp;
	 all = all->next;
 }
 return copyList;
}



// compute the union of two DLLists u and v

// Let u = DLList u->size and v = v->size
// Then Time Complexity is O(u*v)
DLList *setUnion(DLList *u, DLList *v)
{
 // put your code here
 DLList *DA = cloneList(u);
 //DLList *DB = cloneList(v);
 DLListNode *DA_current = DA->first;
 DLListNode *DB_current = v->first;
 //printf("%d",DB_current->next->value);
 //int add_value;
 //char *ss = "passed";
 //printf("%d",DB_current->next->value);
 while(DB_current != NULL){		//roop v times
	 int flag = 1;
	 //printf("%d",DB_current->next->value);
	 //printf("%d\n",DA_current->value);
	 while(DA_current != NULL){		//roop u times
		 //printf("%d %d\n",DA_current->value,DB_current->value);
		 if(DA_current->value == DB_current->value){
			 flag = 0;
			 //printf("%s\n",ss);
		 }
		 DA_current = DA_current->next;
	 }
	 //A need to return first
	 DA_current = DA->first;
	 //printf("%d",DB_current->next->value);
	 if(flag == 1){
		 DLListNode *add_Node = newDLListNode(DB_current->value);
		 DA->last->next = add_Node;
		 add_Node->prev = DA->last;
		 DA->last = add_Node;
		 DA->size ++;
	 }
	 //printf("%d",DB_current->next->value);
	 DB_current = DB_current->next;
	 //printf("%d",DB_current->value);
	 //freeDLList(DB);
 }
 return DA;
}




// compute the insection of two DLLists u and v
// put your time complexity analysis for intersection() here
// Let u = DLList u->size and v = v->size
// Then Time Complexity is O(u*v)
DLList *setIntersection(DLList *u, DLList *v)
{
  // put your code here
	DLList *IDLL = newDLList();
	DLListNode *all = NULL;
	DLListNode *DA_current = u->first;
	DLListNode *DB_current = v->first;
	//char *ss = "passed";
	while(DB_current != NULL){					//roop v times
		int flag = 0;
		while(DA_current != NULL){
			if(DA_current->value == DB_current->value){				//roop u times
				flag = 1;
			}
			DA_current = DA_current->next;
		}
		//A need to return first
		DA_current = u->first;
		if(flag == 1){
			DLListNode *new = newDLListNode(DB_current->value);
			if(IDLL->first == NULL){
				IDLL->first = new;
			}
			all = joinDLL(all,new);
			IDLL->size ++;
		}
		DB_current = DB_current->next;
	}

	while(all != NULL){
 	 if(all->next == NULL){
 		 IDLL->last = all;
 	 }
 	 all = all->next;
  }
	return IDLL;
}


// free up all space associated with list
// put your time complexity analysis for freeDLList() here

//Let n = L->size
//Time Complexity is O(n)
void freeDLList(DLList *L)
{
	DLListNode *p = L->first;
	while(p!=NULL){				//n times roop
		DLListNode *temp = p->next;
		free(p);
		p = temp;
	}
	free(L);
// put your code here
}


// display items of a DLList
// put your time complexity analysis for printDDList() here
//Let n = u->size
//Then Time Complexity is O(n)
void printDLList(DLList *u)
{
	DLListNode *p;
	for(p = u->first;p != NULL;p = p->next){			//n times roop
		printf("%d",p->value);
		putchar('\n');
		/*
		if(p->next != NULL){
			printf("->");
		}
		*/
	}
	putchar('\n');
	//putchar('\n');
 // put your code here
}


// for print tail to head
/*
void printDLList(DLList *u)
{
	DLListNode *p;
	for(p = u->last;p != NULL;p = p->prev){
		printf("%d",p->value);
		if(p->prev != NULL){
			printf("<-");
		}
	}
	putchar('\n');
 // put your code here
}
*/


int main()
{
 DLList *list1, *list2, *list3, *list4;
 //DLList *list1,*list2;


 list1=CreateDLListFromFileDlist("File1.txt");
 //printf("Size is:%d\n",list1->size);
 //printf("last is:%d\n",list1->last->value);
 printDLList(list1);

 list2=CreateDLListFromFileDlist("File2.txt");
 //printf("Size is:%d\n",list2->size);
 printDLList(list2);


 list3=setUnion(list1, list2);
 printDLList(list3);

 list4=setIntersection(list1, list2);
 printDLList(list4);


 freeDLList(list1);
 freeDLList(list2);
 freeDLList(list3);
 freeDLList(list4);

 printf("please type all the integers of list1\n");
 list1=CreateDLListFromFileDlist("stdin");
 //printDLList(list1);

 printf("please type all the integers of list2\n");
 list2=CreateDLListFromFileDlist("stdin");
 //printDLList(list2);

 list3=cloneList(list1);
 printDLList(list3);
 list4=cloneList(list2);
 printDLList(list4);

 freeDLList(list1);
 freeDLList(list2);
 freeDLList(list3);
 freeDLList(list4);


 return 0;
}
