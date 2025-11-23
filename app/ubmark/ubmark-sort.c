//========================================================================
// ubmark-sort
//========================================================================

#include "ubmark-sort.h"

//------------------------------------------------------------------------
// ubmark_sort
//------------------------------------------------------------------------

void ubmark_sort( int* x, int size )
{


  for ( int i = 1; i < size; i++ ) {

    // Load element once into a register
    int key = x[i];

    int j = i - 1;

    // Shift larger elements to the right
    while ( j >= 0 && x[j] > key ) {
      x[j+1] = x[j];   // 1 load + 1 store per iteration
      j--;
    }

    // Write key into correct location
    x[j+1] = key;
  }
}

