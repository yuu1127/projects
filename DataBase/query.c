// query.c ... query scan functions
// part of Multi-attribute Linear-hashed Files
// Manage creating and using Query objects
// Last modified by John Shepherd, July 2019

#include "defs.h"
#include "query.h"
#include "reln.h"
#include "tuple.h"
#include "hash.h"
#include "page.h"
#include <math.h>

// A suggestion ... you can change however you like
#define HEADERSIZE (2*sizeof(Count)+sizeof(Offset))

struct QueryRep {
	Reln    rel;       // need to remember Relation info
	Bits    known;     // the hash value from MAH
	Bits    unknown;   // the unknown bits from MAH
	PageID  curpage;   // current page in scan
	int     is_ovflow; // are we in the overflow pages?
	Offset  curtup;    // offset of current tuple within page
	int     curstar;
	int     nstars;
	char    query[MAXTUPLEN];
    char    curtupStr[MAXTUPLEN];
    Bits* buckets;
	//TODO

};


/*
 * Use queue to process each unknown bit
 * Queue code from: https://www.tutorialspoint.com/data_structures_algorithms/queue_program_in_c
 */
Bits* findAllBuckets(Reln r, Bits known, Bits unknown, int nstars)
{
//    char buf[MAXBITS+1];
    int bucketsTotal = pow(2, nstars);

    // buff as a queue
    int buffCount = 0;
    int front = 0;
    int rear = -1;
    Bits* buff = (Bits *) malloc(bucketsTotal * sizeof(Bits));

    // no unknown bits => only one bucket which is known bit
    if (nstars == 0) {
        buff[0] = known;

        return buff;
    }

    // start the
    buff[++rear] = 0;
    buffCount++;

    for (int unkIndex = 0; unkIndex < depth(r) + 1; ++unkIndex) {
        if (bitIsSet(unknown, unkIndex)) {
            int i = buffCount;
            while (i != 0) {
                // get first element of buff queue
                Bits element = buff[front++];
                if (front == bucketsTotal) {
                    front = 0;
                }
                buffCount--;

                // Replace with 0 and 1, add back to queue
                if(rear == bucketsTotal - 1) {
                    rear = -1;
                }
                buff[++rear] = setBit(known | element, unkIndex);
                buffCount++;

                if(rear == bucketsTotal - 1) {
                    rear = -1;
                }
                buff[++rear] = unsetBit(known | element, unkIndex);
                buffCount++;

                i--;
            }
        }
    }

    return buff;
}

//Bits hashToPageNum(Bits known,Bits unknown,Count k)
//{
//    //TODO:how to use unkownbits
//    Bits mask = (known >> (MAXCHVEC - k));
//    return(known | mask);
//}

// take a query string (e.g. "1234,?,abc,?")
// set up a QueryRep object for the scan

Query startQuery(Reln r, char *q)
{
	Query new = malloc(sizeof(struct QueryRep));
	assert(new != NULL);
    char buf[MAXBITS+1];
    strcpy(new->query,q);
    //printf("%s\n",new->query);

	new->nstars = 0;
    new->rel = r;
    new->known = 0;
    new->unknown = 0;
    Bits h;
    //Bits composite_hash = 0;
    // index is attribute index (if number of attribute = 3 index is 0~2)
    int index = 0;
    int position = 0;
    char *attr = strtok(q, ",");
    while(attr != NULL){
        position = 0;
        //printf("%s is:" ,attr);
        //for each attribute
        h = hash_any((unsigned char *)attr,strlen(attr));
//        bitsString(h,buf);
//        printf("%s\n",buf);
        if(strcmp(attr,"?") != 0){
            for(int j=0;j < MAXCHVEC;j++) {
                // first check index cmp
                if (index == chvec(r)[j].att){
                    // then bit check
                    if (bitIsSet(h, chvec(r)[j].bit) == 1) {
                        //TODO:position is correct or not
                        //printf("1set\n");
                        //composite_hash = setBit(composite_hash, position);
                        new->known = setBit(new->known, position);
                        //new->unknown = unsetBit(new->unknown, position);
                    }
                    else {
                        //printf("0set\n");
                        //composite_hash = unsetBit(composite_hash, position);
                        //TODO is it necessary?
                        new->known = unsetBit(new->known, position);
                        //new->unknown = unsetBit(new->unknown, position);
                    }
                }
                else{
                    //ignore choicevec
                }
                position++;
            }
        }
        else {
            for (int k = 0; k < MAXCHVEC; k++) {
                // index check for attribut(A,B) for A
                if (index == chvec(r)[k].att) {
                    //printf("star1set\n");
                    //new->known = unsetBit(new->known, position);
                    new->unknown = setBit(new->unknown, position);
                    if(position < depth(r) + 1) {
                        new->nstars++;
                    }
                }
                position++;
            }
        }
        //TODO:make else here ***
        attr = strtok(NULL,",");
        index++;
    }
    //printChVec(chvec(r));
//    bitsString(composite_hash,buf);
//    printf("c_hash:");
//    printf("%s\n",buf);
    printf("know bits:");
    bitsString(new->known,buf);
    printf("%s\n",buf);
    printf("unknown bits:");
    bitsString(new->unknown,buf);
    printf("%s\n",buf);
    // getLower() + 1 is need or not if d bit , the number of size is 2^d bit pages
    if(depth(r) == 0){
        new->curpage = 1;
    }
    else {
        new->curpage = getLower(new->known, depth(r));
        // なんで?
        // left ones already splitedd:
        if (new->curpage < splitp(r)) {
            new->curpage = getLower(new->known, depth(r) + 1);
        }
    }

//    bitsString(new->curpage,buf);
//    printf("curpage:%s\n",buf);

    //Page pg = getPage(dataFile(r),new->curpage);
    new->is_ovflow = FALSE;
//    if(pageOvflow(pg) == NO_PAGE) {
//        new->is_ovflow = 0;
//    }
//    else{
//        new->is_ovflow = 1;
//    }
//    printf("is_overflow:%d\n",new->is_ovflow);

    // curtup is right or not ?
    new->curtup = 0;
    new->curstar = 0;
    //printf("curtup:%s\n",pageData(pg));
    //printf("curtup:%d\n",pageData(pg)[0]);
    // new->curstar = = 0;
    //new->nstars = pow(2,new->nstars);
    new->buckets = findAllBuckets(r, new->known, new->unknown, new->nstars);

//    for(int i = 0;i < pow(2,new->nstars);i++){
//        bitsString(new->buckets[i],buf);
//        PageID  j = getLower(new->buckets[i], depth(r));
//        if(j < splitp(r)){
//            j = getLower(new->buckets[i],depth(r) + 1);
//        }
//        printf("%s, PageId: %d\n", buf,j);
//    }
    //printf("query is %s\n", new->query);


	// TODO
	// Partial algorithm:
	// form known bits from known attributes
	// form unknown bits from '?' attributes
	// compute PageID of first page
	//   using known bits and first "unknown" value
	// set all values in QueryRep object
	return new;
}

// map hash into page
// get next tuple during a scan

//void MoveBucket(Query q){
//    int check = q->curstar % 2;
//    if(check == 0){
//        int position = getfirst1(unknown);
//    }
//    q->curtup = 0;
//    q->curpage
//    q->known
//    q->unknown
//    q->curstar++;
//}

Tuple getNextTuple(Query q)
{
    // TODO just make Backets
    //printf("star:%d,%d\n",q->curstar,q->nstars);
    Reln r = q->rel;
    char *t1 = q->query;
    //printf("tuple:%d,%d\n",q->curtup,ntups);
	for(int i = q->curstar;i < pow(2,q->nstars);i++) {
        Page pg;
        if (!q->is_ovflow) {
            if (q->curtup == 0) {
                q->curpage = getLower(q->buckets[i], depth(r));
                if(q->curpage < splitp(r)){
                    q->curpage = getLower(q->buckets[i],depth(r) + 1);
                }
                else{
                    // なんで？　ｗｈｙ bitisset ?
                    // skip duplicate
                    if(bitIsSet(q->buckets[i],depth(r))){
                        q->curstar++;
                        // go to next roop
                        continue;
                    }
                }
            }
            pg = getPage(dataFile(r), q->curpage);
        } else {
            pg = getPage(ovflowFile(r), q->curpage);
        }
        //Count ntups = pageNTuples(pg);
        // be careful * place different
        //char buf[MAXBITS + 1];
        // start scan bucket
        char *data = pageData(pg);
        char *t2;
        //  なんで？
        Offset end = PAGESIZE - pageFreeSpace(pg) - HEADERSIZE;
        for (Offset j = q->curtup; j < end; j++) {
            // get tuple value
            t2 = data + j;
            //printf("error1!! \n");
            //printf("%d,%d\n",q->curtup,ntups);
            //printf("%s\n", t1);
            //printf("%s\n", t2);
            if (tupleMatch(r, t1, t2) == TRUE) {
                //printf("error2!! \n");
                q->curtup = j + strlen(t2) + 1;
                strcpy(q->curtupStr, t2);
                free(pg);
                //return t2;
                return q->curtupStr;
            }
            else {
                j += strlen(t2);
            }
        }
        //free(pg);
        q->curtup = 0;
        Page ovpg;
        PageID ovp;
        ovp = pageOvflow(pg);
        free(pg);
        //if overflow
        while (ovp != NO_PAGE) {
            //printf("Go to Ovflow\n");
            q->is_ovflow = TRUE;
            q->curpage = ovp;
            ovpg = getPage(ovflowFile(r), q->curpage);
            data = pageData(ovpg);
            Offset end = PAGESIZE - pageFreeSpace(ovpg) - HEADERSIZE;
            //Count ntups = pageNTuples(ovpg);
            for (Offset k = q->curtup; k < end; k++) {
                // get tuple value
                t2 = data + k;
                if (tupleMatch(r, t1, t2) == TRUE) {
                    //t2 += strlen(t2) + 1;
                    q->curtup = k + strlen(t2) + 1;
                    strcpy(q->curtupStr, t2);
                    free(ovpg);
                    //return t2;
                    return q->curtupStr;
                }
                else {
                    k += strlen(t2);
                }
            }
            ovp = pageOvflow(ovpg);
            free(ovpg);
            q->curtup = 0;
        }
        // MoveBacket(q);
        // reset is_overflow before moving to next bucket
        q->is_ovflow = FALSE;
        q->curstar++;
	}
	// Partial algorithm:
	// if (more tuples in current page)
	//    get next matching tuple from current page
	// else if (current page has overflow)
	//    move to overflow page
	//    grab first matching tuple from page
	// else
	//    move to "next" bucket = move to next *(0,1) ?
	//    grab first matching tuple from data page
	// endif
	// if (current page has no matching tuples)
	//    go to next page (try again)
	// endif
	return NULL;
}

// clean up a QueryRep object and associated data

void closeQuery(Query q)
{
	// TODO
	free(q->buckets);
	free(q);
}
