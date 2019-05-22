#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

// This template is only a guide
// You need to include additional fields, data structures and functions
// input then make tree(task schedule)

// data type for heap nodes
typedef struct HeapNode {
	// each node stores the priority (key), name, execution time,
	//  release time and deadline of one task
	int key; //key of this task
	int TaskName;  //task name
	int Etime; //execution time of this task
	int Rtime; // release time of this task
	int Dline; // deadline of this task
	// ... // add additional fields here
	int degree;
	struct HeapNode *first_child;
	struct HeapNode *sibling;
} HeapNode;

//data type for a priority queue (heap)
typedef struct BinomialHeap{ //this is heap header
	int  size;      // count of items in the heap
	//... // add additional fields here
	HeapNode *root;
} BinomialHeap;

// create a new heap node to store an item (task)
HeapNode *newHeapNode(int k, int n, int c, int r, int d)
{ // k:key, n:task name, c: execution time, r:release time, d:deadline
  // ... you need to define other parameters yourself)
	HeapNode *new;
	new = malloc(sizeof(HeapNode));
	assert(new != NULL);
	new->key = k;
	new->TaskName = n;
	new->Etime = c;
	new->Rtime = r;
	new->Dline = d;
	// ... // initialise other fields
	new->degree = 0;
	new->first_child = NULL;
	new->sibling = NULL;
	return new;
}

// create a new empty heap-based priority queue
BinomialHeap *newHeap()
{ // this function creates an empty binomial heap-based priority queue
	BinomialHeap *T;
	T = malloc(sizeof(BinomialHeap));
	assert (T != NULL);
	//... // initialise all the fields here
	T->size = 0;
	T->root = NULL;
	return T;
}

//each tree has maximum log(n) then O(log(n))
HeapNode *heap_merge(HeapNode *H1, HeapNode *H2) {
    if(H1 == NULL){
			return H2;
		}
		if(H2 == NULL){
			return H1;
		}

		HeapNode *head;
		HeapNode *tail;

		if(H1->degree <= H2->degree){
			head = H1;
			H1 = H1->sibling;
		}
		else{
			head = H2;
			H2 = H2->sibling;
		}

		tail = head;

		while(H1 != NULL && H2 != NULL){

			if(H1->degree <= H2->degree){
				tail->sibling = H1;
				H1 = H1->sibling;
			}
			else{
				tail->sibling = H2;
				H2 = H2->sibling;
			}
			tail = tail->sibling;
		}

		if(H1 != NULL){
			tail->sibling = H1;
		}
		else{
			tail->sibling = H2;
		}
		return head;
}

// to make link h1 h2
void heap_link(HeapNode *H1, HeapNode *H2) {
    H1->sibling = H2->first_child;
    H2->first_child = H1;
    H2->degree = H2->degree + 1;
}

HeapNode *heap_union(HeapNode *H1, HeapNode *H2) {
		if(H1 == NULL){
			return H2;
		}
		//printf("ななさま\n");
    HeapNode *prev;
    HeapNode *next;
    HeapNode *x;
    HeapNode *H;
		H = heap_merge(H1, H2);
    if (H == NULL){
			return H;
		}
    prev = NULL;
    x = H;
    next = x->sibling;
    while (next != NULL) {
        if ((x->degree != next->degree) || ((next->sibling != NULL)
                && (next->sibling)->degree == x->degree)) {
            prev = x;
            x = next;
        }
				else {
            if (x->key <= next->key) {
                x->sibling = next->sibling;
                heap_link(next, x);
            }
						else {
                if(prev == NULL){
									H = next;
								}
                else{
									prev->sibling = next;
								}
                heap_link(x, next);
                x = next;
            }
        }
        next = x->sibling;
    }
    return H;
}


//use for merge
// put the time complexity analysis for Insert() here
//time complexity O(log(n)) because of union(merge)
void Insert(BinomialHeap *T, int k, int n, int c, int r, int d)
{ // k: key, n: task name, c: execution time, r: release time, d:deadline
  // You don't need to check if this task already exists in T
  //put your code here
	HeapNode *H1;
	//printf("hh%d",T->size);
	H1 = T->root;
	T->size += 1;
	HeapNode *H2 = newHeapNode(k,n,c,r,d);
	//printf("hh%d",T->size);
	T->root = heap_union(H1,H2);
	//H1 = だと絶対ダメ　なんで？
}

// use for Removemin find min(root) to use O(log(n))trees = O(log(n))
void heap_remove(BinomialHeap *T, HeapNode *min_node, HeapNode *min_prev)
{
	if( min_node == T->root ){
		T->root = min_node->sibling;
	}
	else{
		min_prev->sibling = min_node->sibling;
	}

	HeapNode *new_head = NULL;
	HeapNode *child = min_node->first_child;

	while( child != NULL )
	{
		HeapNode *next = child->sibling;
		child->sibling = new_head;
		new_head = child;
		child = next;
	}

	BinomialHeap *temp = newHeap();
	temp->root = new_head;
	T->root = heap_union(T->root, temp->root);
	free(temp);
}

//use for merge
// put your time complexity for RemoveMin() here
//time complexity O(log(n)) (because of tree search)
HeapNode *RemoveMin(BinomialHeap *T)
{
 // put your code here
 if(T->root == NULL){
	 return NULL;
 }
 int min;
 HeapNode *min_node = T->root;
 HeapNode *min_prev = NULL;
 HeapNode *next = min_node->sibling;
 HeapNode *next_prev = min_node;

 while(next != NULL){
	 if(next->key < min_node->key){
		 min_node = min_node->sibling;
		 min_prev = next_prev;
	 }
	 next_prev = next;
	 next = next->sibling;
 }

 heap_remove(T,min_node,min_prev);
 T->size -= 1;
 return min_node;
}


//time complexity O(log(n))
// same as removemin O(log n) trees
int Min(BinomialHeap *T)
{
  // put your code here
	if(T->root == NULL){
		return 0;
	}
	int min;
	HeapNode *min_node = T->root;
	HeapNode *min_prev = NULL;
	HeapNode *next = min_node->sibling;
	HeapNode *next_prev = min_node;
	//find minimum root
	while(next != NULL){
		if(next->key < min_node->key){
			min_node = min_node->sibling;
			min_prev = next_prev;
		}
		next_prev = next;
		next = next->sibling;
	}
	min = min_node->key;
	return min;
}


// put your time complexity analysis for MyTaskScheduler here
// time complexity O(n * log(n)) (n roop * log(n) insert)
// for R_Heap and D_Heap
int TaskScheduler(char *f1, char *f2, int m )
{
 // put your code here
 	char buffer[100];
 	FILE *fp1;
	FILE *fp2;
	int n;
	int c;
	int r;
	int d;
	//int ch;
 	fp1 = fopen(f1,"r");
 	if(fp1 == NULL){
 		printf("file1 does not exist\n");
		fclose(fp1);
		exit(-1);
	}
	fp2 = fopen(f2,"w");
	BinomialHeap *R_Heap = newHeap();
	//printf("ffff\n");
	while(fscanf(fp1, "%d%*c%d%*c%d%*c%d", &n,&c,&r,&d) != EOF){
		//fprintf(fp2,"%d %d %d %d\n",n,c,r,d);
		//printf("ffff\n");
		if(n >= 0 && c > 0 && r >= 0 && d > 0){
			Insert(R_Heap,r,n,c,r,d);
		}
		else{
			printf("input error when reading the attribute of the task %d\n",n);
			fclose(fp1);
			exit(-1);
		}
		//R_Heap->size += 1;
	}

	BinomialHeap *D_Heap = newHeap();
	int current_time = 0;
	int i;
	//m = 2;
	int core[100];
	//core[0] = 0;
	//core[1] = 0;
	for(i=0 ;i < m; i++){
		core[i] = 0;
	}
	int execute_time = 0;
	int ready_time;
	int flag = 0;
	//printf("%d\n",R_Heap->root->Rtime);

	while(R_Heap->size != 0 || D_Heap->size != 0){
		ready_time = Min(R_Heap);
		//printf("%d\n",ready_time);
		//if ready_time <= current_time task is ready to start
		//make D_Heap
		while(R_Heap->size != 0 && ready_time <= current_time){
			//printf("通ってます1\n");
			HeapNode *ex = RemoveMin(R_Heap);
			//printf("通ってます2\n");
			//printf("%d\n",ex->Dline);
			//printf("通ってます3\n");
			Insert(D_Heap,ex->Dline,ex->TaskName,ex->Etime,ex->Rtime,ex->Dline);
			free(ex);
			ready_time = Min(R_Heap);
		}

		//if core > current_time means core already active
		for(i = 0;i < m; i++){
			if(core[i] <= current_time && D_Heap->size != 0){
				HeapNode *do_task = RemoveMin(D_Heap);
				//printf("deadtime:%d\n",do_task->Dline);

				//core[i] = core[i] + do_task->Etime;
				core[i] = current_time + do_task->Etime;
				//printf("core[%d] time start is %d and end is %d\n",i,current_time,core[i]);
				if(do_task->Dline < core[i]){
					flag = 1;
				}
				fprintf(fp2,"%d core%d %d\n",do_task->TaskName,i + 1,current_time);
				free(do_task);
			}
		}
		//printf("通ってます4\n");
		current_time += 1;
	}
	//printf("通ってます5\n");
	free(R_Heap);
	free(D_Heap);
	fclose(fp1);
	fclose(fp2);
	if(flag == 1){
		return 0;
	}
	else{
		return 1;
	}
}

int main() //sample main for testing
{ int i;
  i=TaskScheduler("samplefile1.txt", "feasibleschedule1.txt", 4);
  if (i==0) printf("No feasible schedule!\n");
  /* There is a feasible schedule on 4 cores */
  i=TaskScheduler("samplefile1.txt", "feasibleschedule2.txt", 3);
  if (i==0) printf("No feasible schedule!\n");
  /* There is no feasible schedule on 3 cores */
  i=TaskScheduler("samplefile2.txt", "feasibleschedule3.txt", 5);
  if (i==0) printf("No feasible schedule!\n");
  /* There is a feasible schedule on 5 cores */
  i=TaskScheduler("samplefile2.txt", "feasibleschedule4.txt", 4);
  if (i==0) printf("No feasible schedule!\n");
  /* There is no feasible schedule on 4 cores */
  i=TaskScheduler("samplefile3.txt", "feasibleschedule5.txt", 2);
  if (i==0) printf("No feasible schedule!\n");
  /* There is no feasible schedule on 2 cores */
  i=TaskScheduler("samplefile4.txt", "feasibleschedule6.txt", 2);
  if (i==0) printf("No feasible schedule!\n");
  /* There is a feasible schedule on 2 cores */
 return 0;
}
