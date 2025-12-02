//========================================================================
// ubmark-sort-helper-test
//========================================================================
// Unit tests for ubmark_sort (insertion sort)
//========================================================================

#include "ece4750.h"
#include "ubmark-sort.h"

//------------------------------------------------------------------------
// test_basic_sort
//------------------------------------------------------------------------

void test_basic_sort()
{
  ECE4750_CHECK( L"test_basic_sort" );

  int x[]     = { 5, 2, 6, 1, 4, 3 };
  int x_ref[] = { 1, 2, 3, 4, 5, 6 };

  ubmark_sort( x, 6 );

  for ( int i = 0; i < 6; i++ ) {
    ECE4750_CHECK_INT_EQ( x[i], x_ref[i] );
  }
}

//------------------------------------------------------------------------
// test_already_sorted
//------------------------------------------------------------------------

void test_already_sorted()
{
  ECE4750_CHECK( L"test_already_sorted" );

  int x[]     = { 1, 2, 3, 4, 5 };
  int x_ref[] = { 1, 2, 3, 4, 5 };

  ubmark_sort( x, 5 );

  for ( int i = 0; i < 5; i++ ) {
    ECE4750_CHECK_INT_EQ( x[i], x_ref[i] );
  }
}

//------------------------------------------------------------------------
// test_reverse_sorted
//------------------------------------------------------------------------

void test_reverse_sorted()
{
  ECE4750_CHECK( L"test_reverse_sorted" );

  int x[]     = { 6, 5, 4, 3, 2, 1 };
  int x_ref[] = { 1, 2, 3, 4, 5, 6 };

  ubmark_sort( x, 6 );

  for ( int i = 0; i < 6; i++ ) {
    ECE4750_CHECK_INT_EQ( x[i], x_ref[i] );
  }
}

//------------------------------------------------------------------------
// test_single_element
//------------------------------------------------------------------------

void test_single_element()
{
  ECE4750_CHECK( L"test_single_element" );

  int x[] = { 42 };

  ubmark_sort( x, 1 );

  ECE4750_CHECK_INT_EQ( x[0], 42 );
}

//------------------------------------------------------------------------
// main
//------------------------------------------------------------------------

int main()
{
  test_basic_sort();
  test_already_sorted();
  test_reverse_sorted();
  test_single_element();

  return 0;
}