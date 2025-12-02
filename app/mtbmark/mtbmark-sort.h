//========================================================================
// mtbmark-sort
//========================================================================
// This microbenchmark sorts an array of integers.

#ifndef MTBMARK_SORT_H
#define MTBMARK_SORT_H


void mtbmark_sort( int* x, int size );

void merge_two_runs( int* x,
                     int  start1, int len1,
                     int  start2, int len2,
                     int* tmp );

#endif /* MTBMARK_SORT_H */

