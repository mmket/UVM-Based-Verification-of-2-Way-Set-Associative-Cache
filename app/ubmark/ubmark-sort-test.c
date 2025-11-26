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
// test_case_1_sort_basic  (basic correctness)
//------------------------------------------------------------------------

void test_case_1_sort_basic()
{
  ECE4750_CHECK( L"test_case_1_sort_basic" );

  int a[]     = { 4, 3, 6, 5 };
  int a_ref[] = { 3, 4, 5, 6 };

  ubmark_sort( a, 4 );

  for ( int i = 0; i < 4; i++ )
    ECE4750_CHECK_INT_EQ( a[i], a_ref[i] );

  ECE4750_CHECK_INT_EQ( ece4750_get_heap_usage(), 0 );
}

//------------------------------------------------------------------------
// test_case_2_single_element
//------------------------------------------------------------------------

void test_case_2_single_element()
{
  ECE4750_CHECK( L"test_case_2_single_element" );

  int a[]     = { 9 };
  int a_ref[] = { 9 };

  ubmark_sort( a, 1 );

  ECE4750_CHECK_INT_EQ( a[0], a_ref[0] );
  ECE4750_CHECK_INT_EQ( ece4750_get_heap_usage(), 0 );
}

//------------------------------------------------------------------------
// test_case_3_already_sorted
//------------------------------------------------------------------------

void test_case_3_already_sorted()
{
  ECE4750_CHECK( L"test_case_3_already_sorted" );

  int a[]     = { 1, 2, 3, 4, 5 };
  int a_ref[] = { 1, 2, 3, 4, 5 };

  ubmark_sort( a, 5 );

  for ( int i = 0; i < 5; i++ )
    ECE4750_CHECK_INT_EQ( a[i], a_ref[i] );

  ECE4750_CHECK_INT_EQ( is_sorted(a,5), 1 );
  ECE4750_CHECK_INT_EQ( ece4750_get_heap_usage(), 0 );
}

//------------------------------------------------------------------------
// test_case_4_reverse_sorted  (worst-case)
//------------------------------------------------------------------------

void test_case_4_reverse_sorted()
{
  ECE4750_CHECK( L"test_case_4_reverse_sorted" );

  int a[]     = { 9, 7, 5, 3, 1 };
  int a_ref[] = { 1, 3, 5, 7, 9 };

  ubmark_sort( a, 5 );

  for ( int i = 0; i < 5; i++ )
    ECE4750_CHECK_INT_EQ( a[i], a_ref[i] );

  ECE4750_CHECK_INT_EQ( is_sorted(a,5), 1 );
  ECE4750_CHECK_INT_EQ( ece4750_get_heap_usage(), 0 );
}

//------------------------------------------------------------------------
// test_case_5_with_duplicates
//------------------------------------------------------------------------

void test_case_5_with_duplicates()
{
  ECE4750_CHECK( L"test_case_5_with_duplicates" );

  int a[]     = { 5, 3, 5, 3, 5, 1 };
  int a_ref[] = { 1, 3, 3, 5, 5, 5 };

  ubmark_sort( a, 6 );

  for ( int i = 0; i < 6; i++ )
    ECE4750_CHECK_INT_EQ( a[i], a_ref[i] );

  ECE4750_CHECK_INT_EQ( is_sorted(a,6), 1 );
  ECE4750_CHECK_INT_EQ( ece4750_get_heap_usage(), 0 );
}

//------------------------------------------------------------------------
// test_case_6_negative_numbers
//------------------------------------------------------------------------

void test_case_6_negative_numbers()
{
  ECE4750_CHECK( L"test_case_6_negative_numbers" );

  int a[]     = { -3, 1, -9, 2, 0 };
  int a_ref[] = { -9, -3, 0, 1, 2 };

  ubmark_sort( a, 5 );

  for ( int i = 0; i < 5; i++ )
    ECE4750_CHECK_INT_EQ( a[i], a_ref[i] );

  ECE4750_CHECK_INT_EQ( is_sorted(a,5), 1 );
  ECE4750_CHECK_INT_EQ( ece4750_get_heap_usage(), 0 );
}

//------------------------------------------------------------------------
// test_case_7_random_small
//------------------------------------------------------------------------

void test_case_7_random_small()
{
  ECE4750_CHECK( L"test_case_7_random_small" );

  int a[20];
  ece4750_srand(1);

  for (int i = 0; i < 20; i++)
    a[i] = ece4750_rand() & 0x000000ff;

  ubmark_sort(a,20);

  ECE4750_CHECK_INT_EQ( is_sorted(a,20), 1 );
  ECE4750_CHECK_INT_EQ( ece4750_get_heap_usage(), 0 );
}

//------------------------------------------------------------------------
// WHITE-BOX TESTS
//------------------------------------------------------------------------

//------------------------------------------------------------------------
// test_case_8_insert_at_front
//------------------------------------------------------------------------

void test_case_8_insert_at_front()
{
  ECE4750_CHECK( L"test_case_8_insert_at_front" );

  int a[]     = { 9, 1, 5, 7 };
  int a_ref[] = { 1, 5, 7, 9 };

  ubmark_sort( a, 4 );

  for (int i = 0; i < 4; i++)
    ECE4750_CHECK_INT_EQ( a[i], a_ref[i] );
}

//------------------------------------------------------------------------
// test_case_9_insert_middle
//------------------------------------------------------------------------

void test_case_9_insert_middle()
{
  ECE4750_CHECK( L"test_case_9_insert_middle" );

  int a[]     = { 2, 10, 5, 20 };
  int a_ref[] = { 2, 5, 10, 20 };

  ubmark_sort( a, 4 );

  for (int i = 0; i < 4; i++)
    ECE4750_CHECK_INT_EQ( a[i], a_ref[i] );
}

//------------------------------------------------------------------------
// test_case_10_key_stays
//------------------------------------------------------------------------

void test_case_10_key_stays()
{
  ECE4750_CHECK( L"test_case_10_key_stays" );

  int a[]     = { 1, 2, 3, 0 };
  int a_ref[] = { 0, 1, 2, 3 };

  ubmark_sort( a, 4 );

  for (int i = 0; i < 4; i++)
    ECE4750_CHECK_INT_EQ( a[i], a_ref[i] );
}

//------------------------------------------------------------------------
// test_case_11_stable_sort
//------------------------------------------------------------------------

void test_case_11_stable_sort()
{
  ECE4750_CHECK( L"test_case_11_stable_sort" );

  int a[]     = { 3, 1, 3, 2, 3 };
  int a_ref[] = { 1, 2, 3, 3, 3 };

  ubmark_sort( a, 5 );

  for (int i = 0; i < 5; i++)
    ECE4750_CHECK_INT_EQ( a[i], a_ref[i] );
}

//------------------------------------------------------------------------
// test_case_12_multi_shift
//------------------------------------------------------------------------

void test_case_12_multi_shift()
{
  ECE4750_CHECK( L"test_case_12_multi_shift" );

  int a[]     = { 9, 8, 7, 6, 1 };
  int a_ref[] = { 1, 6, 7, 8, 9 };

  ubmark_sort( a, 5 );

  for (int i = 0; i < 5; i++)
    ECE4750_CHECK_INT_EQ( a[i], a_ref[i] );
}

//------------------------------------------------------------------------
// test_case_13_zero_size
//------------------------------------------------------------------------

void test_case_13_zero_size()
{
  ECE4750_CHECK( L"test_case_13_zero_size" );

  int* a = 0;
  ubmark_sort( a, 0 );   // should not crash

  ECE4750_CHECK_INT_EQ( ece4750_get_heap_usage(), 0 );
}

//------------------------------------------------------------------------
// test_case_14_one_size
//------------------------------------------------------------------------

void test_case_14_one_size()
{
  ECE4750_CHECK( L"test_case_14_one_size" );

  int a[] = { 42 };
  ubmark_sort(a,1);

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
  if ( (__n <= 0) || (__n == 7 ) ) test_case_7_random_small();

  if ( (__n <= 0) || (__n == 8 ) ) test_case_8_insert_at_front();
  if ( (__n <= 0) || (__n == 9 ) ) test_case_9_insert_middle();
  if ( (__n <= 0) || (__n == 10 ) ) test_case_10_key_stays();
  if ( (__n <= 0) || (__n == 11 ) ) test_case_11_stable_sort();
  if ( (__n <= 0) || (__n == 12 ) ) test_case_12_multi_shift();
  if ( (__n <= 0) || (__n == 13 ) ) test_case_13_zero_size();
  if ( (__n <= 0) || (__n == 14 ) ) test_case_14_one_size();

  ece4750_wprintf( L"\n\n" );
  return ece4750_check_status;
}