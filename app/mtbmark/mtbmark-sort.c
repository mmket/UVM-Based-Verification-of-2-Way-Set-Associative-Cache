//========================================================================
// mtbmark-sort
//========================================================================

#include "mtbmark-sort.h"
#include "ece4750.h"

// We include ubmark-sort.h so you can call the single-threaded sort
// (which is already tested!) in your multi-threaded sort if you want.

#include "ubmark-sort.h"


#include "ece4750-bthread.h"
#include "ece4750-misc.h"

#define MTBMARK_MAX_SIZE 4096
static int mtbmark_tmpbuf[MTBMARK_MAX_SIZE];

typedef struct {
  int* base;
  int  start;
  int  len;
} sort_task_t;

typedef struct {
  int* x;
  int  start1;
  int  len1;
  int  start2;
  int  len2;
  int* tmp;
} merge_task_t;

static void mtbmark_sort_worker( void* arg )
{
  sort_task_t* t = (sort_task_t*) arg;
  if ( t->len > 0 )
    ubmark_sort( t->base + t->start, t->len );
}

static void mtbmark_merge_worker( void* arg )
{
  merge_task_t* t = (merge_task_t*) arg;
  if ( t->len1 > 0 && t->len2 > 0 )
    merge_two_runs( t->x, t->start1, t->len1,
                    t->start2, t->len2, t->tmp );
}

void merge_two_runs( int* x,
                            int  start1, int len1,
                            int  start2, int len2,
                            int* tmp )
{
  int i    = start1;
  int j    = start2;
  int end1 = start1 + len1;
  int end2 = start2 + len2;
  int k    = 0;

  while ( i < end1 && j < end2 ) {
    if ( x[i] <= x[j] )
      tmp[k++] = x[i++];
    else
      tmp[k++] = x[j++];
  }

  while ( i < end1 )
    tmp[k++] = x[i++];

  while ( j < end2 )
    tmp[k++] = x[j++];

  for ( int t = 0; t < len1 + len2; t++ )
    x[start1 + t] = tmp[t];
}


//------------------------------------------------------------------------
// mtbmark_sort
//------------------------------------------------------------------------

void mtbmark_sort( int* x, int size )
{
  if ( size <= 1 )
    return;

  // If input larger than our static tmp buffer, fall back to single-threaded
  if ( size > MTBMARK_MAX_SIZE ) {
    ubmark_sort( x, size );
    return;
  }

  // We assume 4 workers/cores: 0,1,2,3
  const int nworkers = 4;

  // Partition array into 4 blocks
  sort_task_t tasks[4];

  for ( int w = 0; w < nworkers; w++ ) {
    int start = (size * w)     / nworkers;
    int end   = (size * (w+1)) / nworkers;
    tasks[w].base  = x;
    tasks[w].start = start;
    tasks[w].len   = end - start;
  }

  // Spawn workers on cores 1,2,3 to sort their blocks
  for ( int w = 1; w < nworkers; w++ ) {
    if ( tasks[w].len > 0 )
      ece4750_bthread_spawn( w, mtbmark_sort_worker, &tasks[w] );
  }

  // Core 0 sorts its own block
  if ( tasks[0].len > 0 )
    mtbmark_sort_worker( &tasks[0] );

  // Join workers 1,2,3
  for ( int w = 1; w < nworkers; w++ ) {
    if ( tasks[w].len > 0 )
      ece4750_bthread_join( w );
  }

  // At this point, we have four sorted runs:
  // [0] : [s0 .. s0+len0-1]
  // [1] : [s1 .. s1+len1-1]
  // [2] : [s2 .. s2+len2-1]
  // [3] : [s3 .. s3+len3-1]

  int* tmp = mtbmark_tmpbuf;   // static buffer, no malloc

  int s0 = tasks[0].start;
  int l0 = tasks[0].len;
  int s1 = tasks[1].start;
  int l1 = tasks[1].len;
  int s2 = tasks[2].start;
  int l2 = tasks[2].len;
  int s3 = tasks[3].start;
  int l3 = tasks[3].len;

  // Common case: all four blocks non-empty -> parallelize first two merges
  if ( l0 > 0 && l1 > 0 && l2 > 0 && l3 > 0 ) {

    // Prepare merge task for blocks 2+3 on core 1, using the "back" half of tmp
    merge_task_t mtask1;
    mtask1.x      = x;
    mtask1.start1 = s2;
    mtask1.len1   = l2;
    mtask1.start2 = s3;
    mtask1.len2   = l3;
    mtask1.tmp    = tmp + (l0 + l1);  // disjoint region from the front

    // Spawn merge of blocks 2+3 on core 1
    ece4750_bthread_spawn( 1, mtbmark_merge_worker, &mtask1 );

    // Core 0 merges blocks 0+1 using the front part of tmp
    merge_two_runs( x, s0, l0, s1, l1, tmp );

    // Wait for core 1 to finish merging blocks 2+3
    ece4750_bthread_join( 1 );

    // Now we have two big runs:
    //   Run A: [s0 .. s0 + (l0+l1) - 1]
    //   Run B: [s2 .. s2 + (l2+l3) - 1]

    l0 = l0 + l1;  // combined length of [0]+[1]
    l2 = l2 + l3;  // combined length of [2]+[3]

    // Final merge of the two big runs on core 0
    merge_two_runs( x, s0, l0, s2, l2, tmp );
  }

  // Fallback: if some blocks are empty, use the original sequential merges
  else {

    // Merge block0 + block1
    if ( l0 > 0 && l1 > 0 )
      merge_two_runs( x, s0, l0, s1, l1, tmp );
    else if ( l1 > 0 ) {
      // If block0 empty and block1 non-empty, just treat block1 as the first run
      s0 = s1;
      l0 = l1;
    }
    l0 = l0 + l1; // combined length of [0]+[1]

    // Merge block2 + block3
    if ( l2 > 0 && l3 > 0 )
      merge_two_runs( x, s2, l2, s3, l3, tmp );
    else if ( l3 > 0 ) {
      s2 = s3;
      l2 = l3;
    }
    l2 = l2 + l3; // combined length of [2]+[3]

    // Merge the two big runs: [s0 .. s0+l0-1] and [s2 .. s2+l2-1]
    if ( l0 > 0 && l2 > 0 )
      merge_two_runs( x, s0, l0, s2, l2, tmp );
  }

  // After this, the whole x[0..size-1] is sorted
}

