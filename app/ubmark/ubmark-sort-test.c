//========================================================================
// Unit tests for ubmark sort
//========================================================================

#include "ece4750.h"
#include "ubmark-sort.h"
#include "ubmark-sort.dat"

//------------------------------------------------------------------------
// is_sorted
//------------------------------------------------------------------------
// Helper function that returns 1 if sorted and 0 if unsorted

int is_sorted( int* x, int n )
{
  for ( int i = 0; i < n-1; i++ ) {
    if ( x[i] > x[i+1] )
      return 0;
  }
  return 1;
}

//------------------------------------------------------------------------
// test_case_1_sort_basic
//------------------------------------------------------------------------

void test_case_1_sort_basic()
{
  ECE4750_CHECK( L"test_case_1_sort_basic" );

  int a[]     = { 4, 3, 6, 5, };
  int a_ref[] = { 3, 4, 5, 6, };

  ubmark_sort( a, 4 );

  for ( int i = 0; i < 4; i++ )
    ECE4750_CHECK_INT_EQ( a[i] , a_ref[i] );

  ECE4750_CHECK_INT_EQ( ece4750_get_heap_usage(), 0 );
}

//''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
// Add many more test cases for helper functions and sort function
//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

//------------------------------------------------------------------------
// main
//------------------------------------------------------------------------

int main( int argc, char** argv )
{
  __n = ( argc == 1 ) ? 0 : ece4750_atoi( argv[1] );

  if ( (__n <= 0) || (__n == 1 ) ) test_case_1_sort_basic();

  //''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // Add all test cases here (make sure to check __n appropriately!)
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  ece4750_wprintf( L"\n\n" );
  return ece4750_check_status;
}
