#=========================================================================
# IntMulFL_test
#=========================================================================

import pytest

from random import randint
from random import Random

from pymtl3 import *
from pymtl3.stdlib.test_utils import mk_test_case_table, run_sim
from pymtl3.stdlib.stream import StreamSourceFL, StreamSinkFL

from lab1_imul.IntMulFL import IntMulFL

from random import getrandbits

from random import choice
#-------------------------------------------------------------------------
# TestHarness
#-------------------------------------------------------------------------

class TestHarness( Component ):

  def construct( s, imul ):

    # Instantiate models

    s.src  = StreamSourceFL( Bits64 )
    s.sink = StreamSinkFL( Bits32 )
    s.imul = imul

    # Connect

    s.src.ostream  //= s.imul.istream
    s.imul.ostream //= s.sink.istream

  def done( s ):
    return s.src.done() and s.sink.done()

  def line_trace( s ):
    return s.src.line_trace() + " > " + s.imul.line_trace() + " > " + s.sink.line_trace()

#-------------------------------------------------------------------------
# mk_imsg/mk_omsg
#-------------------------------------------------------------------------

# Make input message, truncate ints to ensure they fit in 32 bits.

def mk_imsg( a, b ):
  return concat( Bits32( a, trunc_int=True ), Bits32( b, trunc_int=True ) )

# Make output message, truncate ints to ensure they fit in 32 bits.

def mk_omsg( a ):
  return Bits32( a, trunc_int=True )

#----------------------------------------------------------------------
# Test Case: small positive * positive
#----------------------------------------------------------------------

small_pos_pos_msgs = [
   mk_imsg(  2,  3 ), mk_omsg(   6 ),
   mk_imsg(  4,  5 ), mk_omsg(  20 ),
   mk_imsg(  3,  4 ), mk_omsg(  12 ),
   mk_imsg( 10, 13 ), mk_omsg( 130 ),
   mk_imsg(  8,  7 ), mk_omsg(  56 ),
]

zero_one_neg_msgs = [
  mk_imsg(  0,  1 ), mk_omsg(   0 ),
  mk_imsg(  0, -1 ), mk_omsg(   0 ),
  mk_imsg(  1,  1 ), mk_omsg(   1 ),
  mk_imsg(  1, -1 ), mk_omsg(  -1 ),
  mk_imsg( -1,  1 ), mk_omsg(  -1 ),
  mk_imsg( -1,  0 ), mk_omsg(   0 ),
  mk_imsg( -1, -1 ), mk_omsg(   1 ),
  mk_imsg(  0,  0 ), mk_omsg(   0 ),
  mk_imsg(  1,  0 ), mk_omsg(   0 ),
]

small_neg_pos_msgs = [
   mk_imsg( -3,  3 ), mk_omsg(  -9 ),
   mk_imsg( -7,  9 ), mk_omsg( -63 ),
   mk_imsg( -6,  7 ), mk_omsg( -42 ),
   mk_imsg(-14,  9 ), mk_omsg(-126 ),
   mk_imsg( -6,  3 ), mk_omsg( -18 ),
]

small_pos_neg_msgs = [
   mk_imsg( 3,  -3 ), mk_omsg(  -9 ),
   mk_imsg( 9,  -7 ), mk_omsg( -63 ),
   mk_imsg( 7,  -6 ), mk_omsg( -42 ),
   mk_imsg( 9, -14 ), mk_omsg(-126 ),
   mk_imsg( 3,  -6 ), mk_omsg( -18 ),
]

small_neg_neg_msgs = [
   mk_imsg( -3,  -3 ), mk_omsg(   9 ),
   mk_imsg( -9,  -7 ), mk_omsg(  63 ),
   mk_imsg( -7,  -6 ), mk_omsg(  42 ),
   mk_imsg( -9, -14 ), mk_omsg( 126 ),
   mk_imsg( -3,  -6 ), mk_omsg(  18 ),
]

large_pos_pos_msgs = [
  mk_imsg( 1446762652,  4567432543 ), mk_omsg( 2519043556 ),
  mk_imsg( 6524278908,  2533757615 ), mk_omsg( 1462301892 ),
  mk_imsg( 5437658716,  5376427652 ), mk_omsg(  265465712 ),
  mk_imsg( 7525438628,  6524687524 ), mk_omsg( 1255213328 ),
  mk_imsg( 6536426982,  2543686865 ), mk_omsg( 2364061894 )
]

large_pos_neg_msgs = [
  mk_imsg( 1446762652,  -4567432543 ), mk_omsg(  1775923740 ),
  mk_imsg( 6524278908,  -2533757615 ), mk_omsg( -1462301892 ),
  mk_imsg( 5437658716,  -5376427652 ), mk_omsg(  -265465712 ),
  mk_imsg( 7525438628,  -6524687524 ), mk_omsg( -1255213328 ),
  mk_imsg( 6536426982,  -2543686865 ), mk_omsg(  1930905402 )
]

large_neg_pos_msgs = [
  mk_imsg( -1446762652,  4567432543 ), mk_omsg(  1775923740 ),
  mk_imsg( -6524278908,  2533757615 ), mk_omsg( -1462301892 ),
  mk_imsg( -5437658716,  5376427652 ), mk_omsg(  -265465712 ),
  mk_imsg( -7525438628,  6524687524 ), mk_omsg( -1255213328 ),
  mk_imsg( -6536426982,  2543686865 ), mk_omsg(  1930905402 )
]

large_neg_neg_msgs = [
  mk_imsg( -1446762652,  -4567432543 ), mk_omsg( -1775923740 ),
  mk_imsg( -6524278908,  -2533757615 ), mk_omsg(  1462301892 ),
  mk_imsg( -5437658716,  -5376427652 ), mk_omsg(   265465712 ),
  mk_imsg( -7525438628,  -6524687524 ), mk_omsg(  1255213328 ),
  mk_imsg( -6536426982,  -2543686865 ), mk_omsg( -1930905402 )
]

low_bit_masked_msgs = [
    mk_imsg(-2113929216, -119537664), mk_omsg(0),
    mk_imsg(-16777216, -90177536), mk_omsg(0),
    mk_imsg(-520093696, -56623104), mk_omsg(0),
    mk_imsg(-2147483648, -945815552), mk_omsg(0),
    mk_imsg(-134217728, -2147483648), mk_omsg(0),
]

middle_bit_masked_msgs = [
    mk_imsg(-2147483647, -536870907), mk_omsg(1610612741),
    mk_imsg(-67108854, -536870908), mk_omsg(2952790056),
    mk_imsg(-134217718, -2147483647), mk_omsg(4160749578),
    mk_imsg(-536870912, -536870898), mk_omsg(1073741824),
    mk_imsg(-2147483633,-1073741816), mk_omsg(1073741944),
]

sparse_number_msgs = [
    mk_imsg(-2146566143, -536608763), mk_omsg(1615462405),
    mk_imsg(-268402422, -536870908), mk_omsg(2147615784),
    mk_imsg(-1006631862, -2147479551), mk_omsg(3292832842),
    mk_imsg(-536870912, -536805362), mk_omsg(1073741824),
    mk_imsg(-2147483633, -1073741432), mk_omsg(1073747704),
]

dense_number_msgs = [
    mk_imsg(-1124074371, -273940491), mk_omsg(939271841),
    mk_imsg(-33576982, -268435468), mk_omsg(2013536520),
    mk_imsg(-67207190, -1), mk_omsg(67207190),
    mk_imsg(-335601665, -327352338), mk_omsg(462602258),
    mk_imsg(-206917473, -548038657), mk_omsg(2331948897),
]

trigger_corner_cases_msgs = [
    mk_imsg(-2146566143, -536608763), mk_omsg(1615462405),
    mk_imsg(-268402422, 536870908), mk_omsg(-2147615784),
    mk_imsg(-1006631862, -2147479551), mk_omsg(3292832842),
    mk_imsg(-536870912, -536805362), mk_omsg(1073741824),
    mk_imsg(-2147483633, 1073741432), mk_omsg(-1073747704),
]

# ----------------------------------------------------------------------
# Random helpers and randomized message sets (reproducible)
# ----------------------------------------------------------------------

_RNG = Random(0x4750)    

INT_MIN = -(1<<31)
INT_MAX =  (1<<31) - 1

def rand_i32():
  return _RNG.randint(INT_MIN, INT_MAX)

def mask_low_bits(x):
  return x & 0xFFFFF000

def mask_high_bits(x):
  return x & 0x000FFFFF

def mask_middle_bits(x):
  mask =0xFF0000FF
  return x & mask

def rand_sparse_i32(p_one=0.10):
  v = 0
  for i in range(31):
    if _RNG.random() < p_one:
      v |= (1 << i)
  if _RNG.random() < 0.5:
    v |= (1 << 31)
  if v & (1<<31):
    return v - (1<<32)
  else:
    return v

def rand_dense_i32(p_one=0.90):
  v = 0
  for i in range(32):
    if _RNG.random() < p_one:
      v |= (1 << i)
  if v & (1<<31):
    return v - (1<<32)
  else:
    return v

def gen_random_msgs(n, make_pair_fn):
  msgs = []
  for _ in range(n):
    a, b = make_pair_fn()
    msgs.extend([ mk_imsg(a,b), mk_omsg(a*b) ])
  return msgs

rand_uniform_msgs = gen_random_msgs(
  50,
  lambda: (rand_i32(), rand_i32())
)

rand_low_masked_msgs = gen_random_msgs(
  50,
  lambda: (
    mask_low_bits(rand_i32()),
    mask_low_bits(rand_i32()),
  )
)

rand_high_masked_msgs = gen_random_msgs(
  50,
  lambda: (
    mask_high_bits(rand_i32()),
    mask_high_bits(rand_i32()),
  )
)

rand_low_high_masked_msgs = gen_random_msgs(
  50,
  lambda: (
    mask_high_bits(mask_low_bits(rand_i32())),
    mask_high_bits(mask_low_bits(rand_i32())),
  )
)

rand_middle_masked_msgs2 = gen_random_msgs(
  50,
  lambda: (mask_middle_bits(rand_i32()), mask_middle_bits(rand_i32()))
)

rand_sparse_msgs = gen_random_msgs(
  50,
  lambda: (rand_sparse_i32(), rand_sparse_i32())
)

rand_dense_msgs = gen_random_msgs(
  50,
  lambda: (rand_dense_i32(), rand_dense_i32())
)


#-------------------------------------------------------------------------
# Test Case Table
#-------------------------------------------------------------------------

test_case_table = mk_test_case_table([
  (                      "msgs                         src_delay sink_delay"),
  [ "small_pos_pos",             small_pos_pos_msgs,        0,        0     ],          
  [ "zero_one_neg_msgs",         zero_one_neg_msgs,         0,        0     ],
  [ "small_neg_pos_msgs",        small_neg_pos_msgs,        0,        0     ],
  [ "small_pos_neg_msgs",        small_pos_neg_msgs,        0,        0     ],
  [ "small_neg_neg_msgs",        small_neg_neg_msgs,        0,        0     ],
  [ "large_pos_pos_msgs",        large_pos_pos_msgs,        0,        0     ],
  [ "large_pos_neg_msgs",        large_pos_neg_msgs,        0,        0     ],
  [ "large_neg_pos_msgs",        large_neg_pos_msgs,        0,        0     ],
  [ "large_neg_neg_msgs",        large_neg_neg_msgs,        0,        0     ],
  [ "low_bit_masked_msgs",       low_bit_masked_msgs,       0,        0     ],
  [ "middle_bit_masked_msgs",    middle_bit_masked_msgs,    0,        0     ],
  [ "sparse_number_msgs",        sparse_number_msgs,        0,        0     ],
  [ "dense_number_msgs",         dense_number_msgs,         0,        0     ],
  [ "trigger_corner_cases_msgs", trigger_corner_cases_msgs, 0,        0     ],
  [ "small_pos_pos",             small_pos_pos_msgs,        1,        3     ],          
  [ "zero_one_neg_msgs",         zero_one_neg_msgs,         2,        2     ],
  [ "small_neg_pos_msgs",        small_neg_pos_msgs,        3,        1     ],
  [ "small_pos_neg_msgs",        small_pos_neg_msgs,        2,        3     ],
  [ "small_neg_neg_msgs",        small_neg_neg_msgs,        1,        1     ],
  [ "large_pos_pos_msgs",        large_pos_pos_msgs,        2,        2     ],
  [ "large_pos_neg_msgs",        large_pos_neg_msgs,        2,        3     ],
  [ "large_neg_pos_msgs",        large_neg_pos_msgs,        3,        1     ],
  [ "large_neg_neg_msgs",        large_neg_neg_msgs,        3,        1     ],
  [ "low_bit_masked_msgs",       low_bit_masked_msgs,       1,        1     ],
  [ "middle_bit_masked_msgs",    middle_bit_masked_msgs,    2,        2     ],
  [ "sparse_number_msgs",        sparse_number_msgs,        1,        3     ],
  [ "dense_number_msgs",         dense_number_msgs,         5,        2     ],
  [ "trigger_corner_cases_msgs", trigger_corner_cases_msgs, 2,        3     ],
  [ "rand_uniform",             rand_uniform_msgs,          0,        0     ],
  [ "rand_low_masked",          rand_low_masked_msgs,       0,        0     ],
  [ "rand_high_masked",         rand_high_masked_msgs,      0,        0     ],
  [ "rand_low_high_masked",     rand_low_high_masked_msgs,  0,        0     ],
  [ "rand_middle_masked2",      rand_middle_masked_msgs2,   0,        0     ],
  [ "rand_sparse",              rand_sparse_msgs,           0,        0     ],
  [ "rand_dense",               rand_dense_msgs,            0,        0     ],
  [ "rand_uniform_delayed",     rand_uniform_msgs,          2,        3     ],
  [ "rand_low_masked_delayed",  rand_low_masked_msgs,       4,        2     ],
  [ "rand_middle_masked_del",   rand_middle_masked_msgs2,   3,        5     ],
  [ "rand_sparse_delayed",      rand_sparse_msgs,           5,        4     ],
  [ "rand_dense_delayed",       rand_dense_msgs,            6,        6     ],

])

#-------------------------------------------------------------------------
# TestHarness
#-------------------------------------------------------------------------

@pytest.mark.parametrize( **test_case_table )
def test( test_params, cmdline_opts ):

  th = TestHarness( IntMulFL() )

  th.set_param("top.src.construct",
    msgs=test_params.msgs[::2],
    initial_delay=test_params.src_delay+3,
    interval_delay=test_params.src_delay )

  th.set_param("top.sink.construct",
    msgs=test_params.msgs[1::2],
    initial_delay=test_params.sink_delay+3,
    interval_delay=test_params.sink_delay )

  run_sim( th, cmdline_opts, duts=['imul'] )