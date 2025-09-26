#=========================================================================
# slt
#=========================================================================

import random

# Fix the random seed so results are reproducible
random.seed(0xdeadbeef)

from pymtl3 import *
from lab2_proc.test.inst_utils import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """
    csrr x1, mngr2proc < 4
    csrr x2, mngr2proc < 5
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    slt x3, x1, x2
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 1
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
  """

#=========================================================================
# slt tests
#=========================================================================

import random
from pymtl3 import *
from lab2_proc.test.inst_utils import *

#-------------------------------------------------------------------------
# gen_dest_dep_test
#-------------------------------------------------------------------------

def gen_dest_dep_test():
  return [
    gen_rr_dest_dep_test( 5, "slt", 1, 2, 1 ),
    gen_rr_dest_dep_test( 4, "slt", 2, 2, 0 ),
    gen_rr_dest_dep_test( 3, "slt", -1 & 0xffffffff, 1, 1 ),  
    gen_rr_dest_dep_test( 2, "slt", 5, -3 & 0xffffffff, 0 ), 
    gen_rr_dest_dep_test( 1, "slt", -5 & 0xffffffff, -3 & 0xffffffff, 1 ), 
    gen_rr_dest_dep_test( 0, "slt", 7, 7, 0 ),
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_test
#-------------------------------------------------------------------------

def gen_src0_dep_test():
  return [
    gen_rr_src0_dep_test( 5, "slt", -8 & 0xffffffff, -7 & 0xffffffff, 1 ),
    gen_rr_src0_dep_test( 4, "slt", -5 & 0xffffffff,  0, 1 ),
    gen_rr_src0_dep_test( 3, "slt",  0, -1 & 0xffffffff, 0 ),
    gen_rr_src0_dep_test( 2, "slt",  5,  10, 1 ),
    gen_rr_src0_dep_test( 1, "slt", 10,  5, 0 ),
    gen_rr_src0_dep_test( 0, "slt",  7,  7, 0 ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_test
#-------------------------------------------------------------------------

def gen_src1_dep_test():
  return [
    gen_rr_src1_dep_test( 5, "slt",  1,  2, 1 ),
    gen_rr_src1_dep_test( 4, "slt",  2,  2, 0 ),
    gen_rr_src1_dep_test( 3, "slt", -1 & 0xffffffff,  1, 1 ),
    gen_rr_src1_dep_test( 2, "slt",  5, -3 & 0xffffffff, 0 ),
    gen_rr_src1_dep_test( 1, "slt", -5 & 0xffffffff, -3 & 0xffffffff, 1 ),
    gen_rr_src1_dep_test( 0, "slt",  7,  7, 0 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_test
#-------------------------------------------------------------------------

def gen_srcs_dep_test():
  return [
    gen_rr_srcs_dep_test( 5, "slt", -8 & 0xffffffff, -7 & 0xffffffff, 1 ),
    gen_rr_srcs_dep_test( 4, "slt", -5 & 0xffffffff,  0, 1 ),
    gen_rr_srcs_dep_test( 3, "slt",  0, -1 & 0xffffffff, 0 ),
    gen_rr_srcs_dep_test( 2, "slt",  5,  10, 1 ),
    gen_rr_srcs_dep_test( 1, "slt", 10,  5, 0 ),
    gen_rr_srcs_dep_test( 0, "slt",  7,  7, 0 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rr_src0_eq_dest_test( "slt", 1, 2, 1 ),
    gen_rr_src1_eq_dest_test( "slt", -2 & 0xffffffff, -1 & 0xffffffff, 1 ),
    gen_rr_src0_eq_src1_test( "slt", 5, 0 ),
    gen_rr_srcs_eq_dest_test( "slt", -3 & 0xffffffff, 0 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_rr_value_test( "slt", 0, 0, 0 ),
    gen_rr_value_test( "slt", 1, 1, 0 ),
    gen_rr_value_test( "slt", 1, 2, 1 ),
    gen_rr_value_test( "slt", 2, 1, 0 ),

    gen_rr_value_test( "slt", -1 & 0xffffffff, 1, 1 ),
    gen_rr_value_test( "slt", 1, -1 & 0xffffffff, 0 ),

    gen_rr_value_test( "slt", -5 & 0xffffffff, -3 & 0xffffffff, 1 ),
    gen_rr_value_test( "slt", -3 & 0xffffffff, -5 & 0xffffffff, 0 ),

    gen_rr_value_test( "slt", 0x7fffffff, -1 & 0xffffffff, 0 ), 
    gen_rr_value_test( "slt", -0x80000000 & 0xffffffff, 0, 1 ), 

  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in range(100):
    src0 = b32( random.randint(0,0xffffffff) )
    src1 = b32( random.randint(0,0xffffffff) )
    dest = b32(1 if src0.int() < src1.int() else 0)
    asm_code.append( gen_rr_value_test( "slt", src0.uint(), src1.uint(), dest.uint() ) )
  return asm_code
