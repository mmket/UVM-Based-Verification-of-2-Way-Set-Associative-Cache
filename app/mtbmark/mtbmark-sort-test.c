//========================================================================
// Unit tests for mtbmark sort
//========================================================================

#include "ece4750.h"
#include "mtbmark-sort.h"
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

  mtbmark_sort( a, 4 );

  for ( int i = 0; i < 4; i++ )
    ECE4750_CHECK_INT_EQ( a[i] , a_ref[i] );

  ECE4750_CHECK_INT_EQ( ece4750_get_heap_usage(), 0 );
}

//------------------------------------------------------------------------
// test_case_2_single_element
//------------------------------------------------------------------------

void test_case_2_single_element()
{
  ECE4750_CHECK( L"test_case_2_single_element" );

  int a[] = { 9 };
  mtbmark_sort( a, 1 );

  ECE4750_CHECK_INT_EQ( a[0], 9 );
  
}

//------------------------------------------------------------------------
// test_case_3_already_sorted
//------------------------------------------------------------------------

void test_case_3_already_sorted()
{
  ECE4750_CHECK( L"test_case_3_already_sorted" );

  int a[]     = { 1,2,3,4,5 };
  int a_ref[] = { 1,2,3,4,5 };

  mtbmark_sort( a, 5 );

  for( int i=0; i<5; i++ )
    ECE4750_CHECK_INT_EQ( a[i], a_ref[i] );
}

//------------------------------------------------------------------------
// test_case_4_reverse_sorted
//------------------------------------------------------------------------

void test_case_4_reverse_sorted()
{
  ECE4750_CHECK( L"test_case_4_reverse_sorted" );

  int a[]     = { 9,8,7,6,5,4,3,2,1 };
  int a_ref[] = { 1,2,3,4,5,6,7,8,9 };

  mtbmark_sort( a, 9 );

  for( int i=0; i<9; i++ )
    ECE4750_CHECK_INT_EQ( a[i], a_ref[i] );
}

//------------------------------------------------------------------------
// test_case_5_with_duplicates
//------------------------------------------------------------------------

void test_case_5_with_duplicates()
{
  ECE4750_CHECK( L"test_case_5_with_duplicates" );

  int a[]     = { 5,1,5,1,5,1,5,1 };
  int a_ref[] = { 1,1,1,1,5,5,5,5 };

  mtbmark_sort( a, 8 );

  for( int i=0; i<8; i++ )
    ECE4750_CHECK_INT_EQ( a[i], a_ref[i] );
}

//------------------------------------------------------------------------
// test_case_6_negative_numbers
//------------------------------------------------------------------------

void test_case_6_negative_numbers()
{
  ECE4750_CHECK( L"test_case_6_negative_numbers" );

  int a[]     = { -3,7,-1,6,-10,2 };
  int a_ref[] = { -10,-3,-1,2,6,7 };

  mtbmark_sort( a, 6 );

  for( int i=0; i<6; i++ )
    ECE4750_CHECK_INT_EQ( a[i], a_ref[i] );
}

//------------------------------------------------------------------------
// test_case_7_uneven_partition
//------------------------------------------------------------------------
// tests multi-core partition correctness (size % 4 != 0)

void test_case_7_uneven_partition()
{
  ECE4750_CHECK( L"test_case_7_uneven_partition" );

  int a[]     = { 7,4,9,1,6 };
  int a_ref[] = { 1,4,6,7,9 };

  mtbmark_sort( a, 5 );

  for( int i=0; i<5; i++ )
    ECE4750_CHECK_INT_EQ( a[i], a_ref[i] );
}

//------------------------------------------------------------------------
// test_case_8_random_small
//------------------------------------------------------------------------

void test_case_8_random_small()
{
  ECE4750_CHECK( L"test_case_8_random_small" );

  int a[20];
  ece4750_srand(123);

  for( int i=0; i<20; i++ )
    a[i] = ece4750_rand() & 0x000000ff;;

  mtbmark_sort( a, 20 );

  ECE4750_CHECK_INT_EQ( is_sorted(a,20), 1 );
}

//------------------------------------------------------------------------
// test_case_9_size_less_than_nworkers
//------------------------------------------------------------------------
// size = 3 → some blocks will be empty

void test_case_9_size_less_than_nworkers()
{
  ECE4750_CHECK( L"test_case_9_size_less_than_nworkers" );

  int a[]     = { 9,3,6 };
  int a_ref[] = { 3,6,9 };

  mtbmark_sort( a, 3 );

  for( int i=0; i<3; i++ )
    ECE4750_CHECK_INT_EQ( a[i], a_ref[i] );
}

//------------------------------------------------------------------------
// test_case_12_zero_size
//------------------------------------------------------------------------

void test_case_12_zero_size()
{
  ECE4750_CHECK( L"test_case_12_zero_size" );

  int* a = 0;
  mtbmark_sort( a, 0 );  // should not crash
}

//------------------------------------------------------------------------
// test_case_13_one_size
//------------------------------------------------------------------------

void test_case_13_one_size()
{
  ECE4750_CHECK( L"test_case_13_one_size" );

  int a[] = { 42 };
  mtbmark_sort( a, 1 );

  ECE4750_CHECK_INT_EQ( a[0], 42 );
}

//------------------------------------------------------------------------
// main
//------------------------------------------------------------------------

int main( int argc, char** argv )
{
  __n = ( argc == 1 ) ? 0 : ece4750_atoi( argv[1] );

  if ( (__n <= 0) || (__n == 1 ) ) test_case_1_sort_basic();
  if ( (__n <= 0) || (__n == 2 ) ) test_case_2_single_element();
  if ( (__n <= 0) || (__n == 3 ) ) test_case_3_already_sorted();
  if ( (__n <= 0) || (__n == 4 ) ) test_case_4_reverse_sorted();
  if ( (__n <= 0) || (__n == 5 ) ) test_case_5_with_duplicates();
  if ( (__n <= 0) || (__n == 6 ) ) test_case_6_negative_numbers();
  if ( (__n <= 0) || (__n == 7 ) ) test_case_7_uneven_partition();
  if ( (__n <= 0) || (__n == 8 ) ) test_case_8_random_small();
  if ( (__n <= 0) || (__n == 9 ) ) test_case_9_size_less_than_nworkers();
  if ( (__n <= 0) || (__n == 12 ) ) test_case_12_zero_size();
  if ( (__n <= 0) || (__n == 13 ) ) test_case_13_one_size();

  ece4750_wprintf( L"\n\n" );
  return ece4750_check_status;
}