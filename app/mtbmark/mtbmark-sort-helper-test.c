//========================================================================
// mtbmark-sort-helper-test
//========================================================================
// Unit tests for merge_two_runs and mtbmark_sort
//========================================================================

#include "ece4750.h"
#include "mtbmark-sort.h"

//------------------------------------------------------------------------
// test_merge_two_runs_basic
//------------------------------------------------------------------------

void test_merge_two_runs_basic()
{
  ECE4750_CHECK( L"test_merge_two_runs_basic" );

  int x[8]   = { 1, 3, 5, 7,  2, 4, 6, 8 };
  int tmp[8] = { 0 };

  merge_two_runs( x, 0, 4,   4, 4, tmp );

  for ( int i = 0; i < 8; i++ ) {
    ECE4750_CHECK_INT_EQ( x[i], i+1 );
  }
}

//------------------------------------------------------------------------
// test_merge_two_runs_edgecase
//------------------------------------------------------------------------

void test_merge_two_runs_edgecase()
{
  ECE4750_CHECK( L"test_merge_two_runs_edgecase" );

  // left block empty
  int x[4]   = { 3, 4, 5, 6 };
  int tmp[4] = { 0 };

  merge_two_runs( x, 0, 0,   0, 4, tmp );

  for ( int i = 0; i < 4; i++ ) {
    ECE4750_CHECK_INT_EQ( x[i], i+3 );
  }
}

//------------------------------------------------------------------------
// test_mtbmark_sort_small
//------------------------------------------------------------------------

void test_mtbmark_sort_small()
{
  ECE4750_CHECK( L"test_mtbmark_sort_small" );

  int x[6]     = { 5, 2, 6, 1, 4, 3 };
  int x_ref[6] = { 1, 2, 3, 4, 5, 6 };

  mtbmark_sort( x, 6 );

  for ( int i = 0; i < 6; i++ ) {
    ECE4750_CHECK_INT_EQ( x[i], x_ref[i] );
  }
}

//------------------------------------------------------------------------
// main
//------------------------------------------------------------------------

int main()
{
  test_merge_two_runs_basic();
  test_merge_two_runs_edgecase();
  test_mtbmark_sort_small();

  return 0;
}